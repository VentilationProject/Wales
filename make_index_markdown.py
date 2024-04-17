import pandas as pd
import os

# Load the data
csv_path = 'schools.csv'
schools_data = pd.read_csv(csv_path)

# Define the output directory for the markdown files
output_dir = './'

# Function to generate an index markdown file in each region directory and a root index file
def create_area_and_root_index():
    # Create a dictionary to keep track of schools and their types in each region
    areas = {}

    for index, row in schools_data.iterrows():
        region_name_simple = row[0].replace(" ", "_").replace("/", "_").replace("\\", "_")
        school_name_simple = row[2].replace(" ", "_").replace("/", "_").replace("\\", "_")
        school_type = row[3]  # Assuming the 'Type' column is the fourth in the DataFrame

        # Check if the region already exists in the dictionary
        if region_name_simple not in areas:
            areas[region_name_simple] = []

        # Append the school name, type, and simple name to the region's list
        areas[region_name_simple].append((school_name_simple, school_type))

    # Write an index markdown file for each region and gather data for root index
    root_index_content = "---\ntitle: School in Wales and their ventilation status\n---\n"

    root_index_content += ("\n# Navigation\n\n[[All countries/states/provinces]](..)\n\n# Purpose of site\n\nGiven **COVID-19 is Airborne** and the world is pushing to better ventilate "
                           "schools for long term student and teacher health, we're tracking the "
                           "progress for that in Wales. This is ahead of government effort to do the same. If government starts to "
                           "track this work, this effort will continue because that effort might might be weak."
                           "We're guided by 33 profs and PhDs who are pushing for a policy change in a "
                           "March 2024 article on **Science.org**: [Mandating indoor air quality for public buildings](https://drive.google.com/file/d/16l_IH47cQtC7fFuafvHca7ORNVGITxx8/view). "
                           "Not only active ventilation (which should "
                           "be mechanical heat recovery type in this age), but air filtration/purification "
                           "too and CO2 monitoring to drive ventilation levels, as CO2 inside is a proxy indicator "
                           "for COVID risk. As it happens the WHO also have a [2023 airborne risk assessment guide](https://iris.who.int/handle/10665/376346)\n\n"
                           "Know that other diseases are airborne too: Measles "
                           "(studies [1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2810934/pdf/10982072.pdf) "
                           "[2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3880795/pdf/nihms532643.pdf) "
                           "[3](https://pubmed.ncbi.nlm.nih.gov/31257413/) "
                           "[4](https://www.sciencedirect.com/science/article/pii/S0196655316305363)), "
                           "Influenza, RSV and TB. The same "
                           "ventilation and air filtration measures reduce transmission of those too.\n\n When we say "
                           "student and teacher health, we're wanting absences to go down too. If we lower "
                           "transmission in schools, we reduce multi-generation transmission too, as kids bring "
                           "infections home to parents. With lowered transmission, we also reduce long COVID, "
                           "where the worst sufferers have disappeared from eduction and the workplace.\n\n")

    root_index_content += ("\n## Leaderboard\n\n1. to be announced\n2. to be announced\n3. to be announced\n4. to be announced\n5. to be announced\n\n")

    root_index_content += ("{% include_relative grade.html %}\n\n")

    root_index_content += ("# Welsh Local Education Authorities:\n\n")

    for area, schools in areas.items():
        area_index_file_path = os.path.join(output_dir, area, "index.md")
        with open(area_index_file_path, 'w') as area_index_file:
            area_index_file.write(f"---\nlayout: page\ntitle: Schools in {area.replace('_', ' ')}\n---\n")
            area_index_file.write(f"# Navigation\n\n[[All countries/states/provinces]](../..) > [[All Welsh educational authorities]](..)\n\n")
            area_index_file.write(f"# Schools in {area.replace('_', ' ')}\n\n")
            area_index_file.write("{% include_relative grade.html %}\n\n")
            area_index_file.write(f"**Schools:**\n\n")
            for school in schools:
                school_file_path = school[0]
                area_index_file.write(f"- [{school[0].replace('_', ' ')}]({school_file_path}): {school[1]}\n")

        # Add to root index content with cleaner URLs
        root_index_content += f"- [{area.replace('_', ' ')}]({area}/): {len(schools)} schools\n"

    root_index_content += ("\n\n# Site ownership\n\nThis site is edited by volunteers who're "
                           "interested in accelerating the work to complete the adequate ventilation of Welsh schools. "
                           "This effort was not commissioned by education authorities or government.\n\n"
                           "[Edit this page](https://github.com/VentilationProject/Wales/edit/prif/index.md). See also [rules for contribution](./contribution_rules/)")

    # Write the root index file
    root_index_path = os.path.join(output_dir, "index.md")
    with open(root_index_path, 'w') as root_index_file:
        root_index_file.write(root_index_content)

# Call the function to create index markdown files and root index
create_area_and_root_index()

# Print confirmation
print("Index markdown files with front matter and links have been created in each area directory and root directory.")