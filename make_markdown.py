import os
import pandas as pd

# Load the data
csv_path = 'schools.csv'
schools_data = pd.read_csv(csv_path)
schools_wikipedia = pd.read_csv("schools_wikipedia.csv", header=0, index_col=[0], squeeze=True).to_dict()
schools_wikidata = pd.read_csv("schools_wikidata.csv", header=0, index_col=[0], squeeze=True).to_dict()
schools_website = pd.read_csv("schools_websites.csv",  header=0, index_col=[0], squeeze=True).to_dict()

# Adjust the address column to replace "+" with ", "
schools_data['Address'] = schools_data['Address'].str.replace('+', ', ', regex=False)

# Define the output directory for the markdown files
output_dir = './'

# Function to generate markdown files
def generate_markdown_by_index(row):
    # Simplify the school name for the directory and file
    region_name_simple = row[0].replace(" ", "_").replace("/", "_").replace("\\", "_")  # Area name is the first column
    school_name_simple = row[2].replace(" ", "_").replace("/", "_").replace("\\", "_")  # School Name is the third column
    path = os.path.join(output_dir, region_name_simple)
    os.makedirs(path, exist_ok=True)

    # Filename for the markdown
    file_path = os.path.join(path, f"{school_name_simple}.md")
    
    # Markdown content with front-matter and details
    with open(file_path, 'w') as file:
        file.write(f"---\nlayout: page\ntitle: {row[2]}\n---\n")  # School Name
        file.write(
            f"# Navigation\n\n[[All countries/states/provinces]](../../..) > [[All Welsh local educational authority]](../..) > [[All schools in local educational authority]](..)\n\n")

        file.write(f"# {row[2]} ({row[0]})\n\n")  # School Name and area as header
        for idx, val in enumerate(row):
            val = str(val)
            if idx not in [0, 2]:  # Skip 'Region' and 'School Name'
                col_name = schools_data.columns[idx].replace('_', ' ')
                if col_name == "Estyn (Schools Inspectorate) URL" and val == "TODO":
                    val = "https://www.estyn.gov.wales/provider/" + str(row[5])
                if col_name == "Wikipedia URL" and val == "TODO" and schools_wikipedia.get(row[2]) is not None:
                    val = schools_wikipedia.get(row[2])
                if col_name == "School Website" and val == "TODO" and schools_website.get(row[2]) is not None:
                    val = schools_website.pop(row[2])
                val = url_to_markdown_link(val)
                if val.endswith(".0"):
                    val = str(round(float(val)))
                elif ", ," in val:
                    val = val.replace(", , ", ", ").replace(", , ", ", ")
                file.write(f"**{col_name}**: {val}\n\n")
        file.write(f"**School's overall airborne virus protection grade (0-5)**: 0\n\n")
        file.write(f"**Discord, Facebook, or WhatsApp group for discovery/advocacy for THIS school**: TODO\n\n")
        file.write(f"**School's policy on Ventilation**: TODO\n\n")
        file.write(f"**School's Ventilation Work Completion**: TODO\n\n")
        file.write(f"**School's Air-Purification**: TODO\n\n")
        file.write(f"**School's CO2 monitoring to actively drive ventilation and filtration**: TODO\n\n")
        file.write(f"**School's Wikidata URL**: ")
        if schools_wikidata.get(row[2]) is not None:
            file.write(url_to_markdown_link(schools_wikidata.get(row[2])) + "\n\n")
        else:
            file.write(f"TODO\n\n")
        file.write(f"\n\n\n[Edit this page](https://github.com/ventilate-schools/Wales/edit/prif/{file_path}).")
        file.write(f" See also [rules for contribution](../../../contribution-rules/)")


def url_to_markdown_link(val):
    if str(val).startswith("https://"):
        val = "[" + val + "](" + val + ")"
    return val


# Apply the function to each row in the DataFrame
schools_data.apply(generate_markdown_by_index, axis=1)

print("Remainder")
print(schools_website)

# Print confirmation
print("Markdown files have been created and are located in:", output_dir)
