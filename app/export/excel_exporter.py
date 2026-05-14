from openpyxl import Workbook

from app.storage.repository import (
    ListingRepository
)


def export_to_excel():

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Listings"

    headers = [
        "ID",
        "Title",
        "Price",
        "Address",
        "Area",
        "Floor",
        "Phone",
        "Status",
        "URL"
    ]

    sheet.append(headers)

    listings = (
        ListingRepository.get_all()
    )

    for item in listings:

        sheet.append([
            item.krisha_id,
            item.title,
            item.price,
            item.address,
            item.area,
            item.floor,
            item.phone,
            item.status,
            item.url
        ])

    file_path = (
        "data/exports/listings.xlsx"
    )

    workbook.save(file_path)

    return file_path