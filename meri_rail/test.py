from bs4 import BeautifulSoup

with open("test.html", "r") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

train_statuses = []
timeline = soup.find("div", id="timeline-1")
blocks = timeline.find_all("div", class_="w3-card-2")

for block in blocks:
    time_container = block.find(
        "div", style=lambda value: value and "text-align: right" in value
    )
    if time_container:
        time_spans = time_container.find_all("span")
        time_info = [span.get_text(strip=True) for span in time_spans]

    station_container = block.find(
        "div", style=lambda value: value and "flex: 1" in value
    )
    if station_container:
        station_spans = station_container.find_all("span")
        station_info = [span.get_text(strip=True) for span in station_spans]

    if time_info and station_info:
        train_statuses.append(
            {
                "station_name": station_info[0],
                "station_code": station_info[1],
                "arrival_time": time_info[0],
                "departure_time": time_info[1],
                "status": station_info[2],
            }
        )

# Print the extracted information
for status in train_statuses:
    print(status)
