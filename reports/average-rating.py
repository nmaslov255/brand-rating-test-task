schema = [("name", str),
	      ("brand", str),
          ("price", int),
          ("rating", float)]


def normalize(records: list[tuple]) -> list[tuple]:
    """
    Нормализует записи по схеме вида:
        [("col_name", str), ("col_name", int), ...]
    Возвращает новый список кортежей.
    Если значение невозможно привести — возбуждает ValidationError.
    """

    header_schema = tuple((name for name, _ in schema))
    body_schema = tuple((_type for _, _type in schema))

    head, body = (records[0], records[1:])
    if head != header_schema:
    	raise Exception(f'Невалидный заголовок {head}, ожидается {header_schema}')

    normalized = []
    for record in body:
        normalized_record = (_type(value) for value, _type in zip(record, body_schema))
        normalized.append(tuple(normalized_record))
    return normalized


def run_processor(records: list[tuple]) -> list[tuple]:
	records = normalize(records)

	# Агрегируем оценки для каждого бренда в списке
	brand_ratings: dict[str, list] = {}
	for name, brand, price, rating in records:
		print('record -> ', name, brand, price, rating)
		try:
			brand_ratings[brand].append(rating)
		except KeyError:
			brand_ratings[brand] = [rating]

	# Считаем среднюю оценку для каждого бренда
	average_brand_rating: list[tuple] = []
	for brand, rating in brand_ratings.items():
		average_brand_rating += (brand, sum(rating))
	return average_brand_rating