from reports.average_rating import Report as AverageRatingReport


def test_average_rating_report_build():
    table = [
        ("name", "brand", "price", "rating"),
        ("Prod1", "BrandA", "100", "4.0"),
        ("Prod2", "BrandB", "200", "3.0"),
        ("Prod3", "BrandA", "150", "5.0"),
    ]

    report = AverageRatingReport(table)
    report_table = report.calculate()

    # Проверяем, что заголовок верный
    assert report_table[0] == ("", "brand", "rating")
    # Проверяем правильность средних значений
    brand_ratings = {record[1]: record[2] for record in report_table[1:]}
    assert brand_ratings["BrandA"] == 4.5  # (4+5)/2
    assert brand_ratings["BrandB"] == 3.0
