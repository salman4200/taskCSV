import csv
from django.shortcuts import render
from .forms import UploadFileForm
from .models import MyModel


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            # Skip the header row
            next(csv_reader)

            success_count = 0
            error_messages = []

            # Start from row 2 (1-based index for error reporting)
            for i, row in enumerate(csv_reader, start=2):
                if len(row) != 6:  # Check if the row has exactly 6 columns
                    error_messages.append(
                        f"Row {i}: Missing columns, expected 6 columns but found {len(row)}")
                    continue

                try:
                    price = float(row[5])  # Convert to float
                except ValueError:
                    error_messages.append(
                        f"Row {i}: Invalid 'Price' value, must be a valid number")
                    continue

                MyModel.objects.create(
                    product_range=row[0],
                    product_group=row[1],
                    style=row[2],
                    item_code=row[3],
                    currency=row[4],
                    price=price
                )
                success_count += 1

            if error_messages:
                return render(request, 'upload.html', {'form': form, 'error_messages': error_messages})
            else:
                return render(request, 'upload_success.html', {'success_count': success_count})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
