import bs4
import fake_headers
import requests
import json


def get_vacancies(query_list: list):
    """
    Retrieves vacancies based on the provided query list and saves the data to a JSON file.

    Args:
        query_list (list): A list of strings representing the search query.

    Returns:
        None
    """
    vacancies = {}
    query = "+".join(query_list)
    url = f'https://spb.hh.ru/search/vacancy?text={query}&area=1&area=2'
    headers = fake_headers.Headers(os='win', browser='chrome').generate()
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    vacancies_list_tag = soup.find(class_="bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-8 bloko-column_l-12")
    vacancy_tags = vacancies_list_tag.find_all(class_="vacancy-serp-item-body")
    for tag in vacancy_tags:
        title = tag.find(class_="bloko-header-section-3").text
        link = tag.find(class_="bloko-link").attrs['href']
        salary_tag = tag.find(class_="bloko-header-section-2")
        if salary_tag is not None:
            salary = " ". join(salary_tag.text.split('\u202f'))
        else:
            salary = "salary not specified"
        company_tag = tag.find(class_="bloko-v-spacing-container bloko-v-spacing-container_base-2")
        company = " ".join(company_tag.text.split('\xa0'))
        city_tag = tag.find_all(class_="bloko-text")
        city = " ".join(city_tag[1].text.split('\xa0'))
        vacancies.setdefault(title, {'Link': link, 'Salary': salary, 'Company': company, 'City': city})
    json_object = json.dumps(vacancies, indent=4, ensure_ascii=False)
    with open("vacancies.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)


get_vacancies(['Python', 'Django', 'Flask'])
