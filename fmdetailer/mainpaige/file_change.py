# main/views.py

import os
import io
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse 
from striprtf.striprtf import rtf_to_text

# Ten widok renderuje szablon HTML z formularzem
def render_file_change(request):
    return render(request, 'file_type_change.html')


# Ten widok obsługuje konwersję i pobieranie pliku
def analyze_file_view(request):
    if request.method != 'POST':
        return redirect('render_file_change') 

    uploaded_file = request.FILES.get('rtf_file')

    if not uploaded_file:
        messages.error(request, 'Nie wybrano żadnego pliku.')
        return redirect('render_file_change')

    original_name = uploaded_file.name
    if not original_name.lower().endswith('.rtf'):
        messages.error(request, 'Przesłany plik nie jest plikiem .rtf.')
        return redirect('render_file_change')
        
    try:
        # === KROK 1: Konwersja RTF na czysty tekst ===
        
        rtf_bytes = uploaded_file.read()
        try:
            # POPRAWKA 1: Najpierw próbujemy dekodować jako UTF-8
            rtf_content = rtf_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Jeśli się nie uda, próbujemy jako latin-1 (lub cp1250)
            rtf_content = rtf_bytes.decode('latin-1')
        
        # Konwersja RTF na czysty tekst
        plain_text = rtf_to_text(rtf_content)

        # === KROK 2: Przetworzenie tekstu na format CSV ===

        lines = [line for line in plain_text.splitlines() if line.strip()]
        
        # Używamy '|' jako separatora
        csv_reader = csv.reader(lines, delimiter='|', quotechar='"')

        output_csv_stream = io.StringIO()
        csv_writer = csv.writer(output_csv_stream, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        for row in csv_reader:
            # POPRAWKA 2: Ulepszony filtr wierszy-separatorów
            # Sprawdzamy, czy wiersz nie jest pusty i czy nie składa się TYLKO z myślników
            is_separator = True
            for cell in row:
                stripped_cell = cell.strip()
                # Sprawdzamy, czy komórka jest pusta LUB składa się tylko z myślników
                if stripped_cell != '' and not all(c == '-' for c in stripped_cell):
                    # Jeśli znajdziemy cokolwiek innego, to NIE jest separator
                    is_separator = False
                    break 
            
            if is_separator:
                continue # Pomiń ten wiersz (to był separator ----)
                
            # Czyszczenie wiersza (usuwanie pustych komórek z początku/końca)
            cleaned_row = [cell.strip() for cell in row if cell.strip()]
            
            if cleaned_row:
                csv_writer.writerow(cleaned_row)

        # === KROK 3: Przygotowanie danych do wysłania ===
        
        csv_string_data = output_csv_stream.getvalue()
        
        # POPRAWKA 3: Kodujemy jako 'utf-8-sig'
        # 'sig' (Signature) dodaje na początku pliku znacznik BOM,
        # który mówi programom (np. Excel), że plik jest w UTF-8.
        csv_bytes_data = csv_string_data.encode('utf-8-sig')

        # Tworzymy nową nazwę pliku
        name_without_ext, _ = os.path.splitext(original_name)
        new_csv_name = name_without_ext + '.csv'

        # === KROK 4: Zwrócenie pliku do pobrania ===
        
        response = HttpResponse(
            csv_bytes_data,
            content_type='text/csv; charset=utf-8-sig'
        )
        response['Content-Disposition'] = f'attachment; filename="{new_csv_name}"'
        
        return response

    except Exception as e:
        messages.error(request, f'Błąd podczas konwersji pliku RTF: {e}')
        return redirect('render_file_change')