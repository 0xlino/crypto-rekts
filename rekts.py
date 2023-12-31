# from the rekt db create a newly format readme of all the rekts

import json
import datetime
import html2text
import time
import os
import urllib.request
# import consts
import subprocess

def rekt_loop(items, start):
    for index, item in enumerate(items[start:], start=start):
        print(f"index: {index} - item: {item['title']}")
        markdownLogo = consts.imageBaseUrl + item['logo_link']
        # format the name for the file so it's nice and pretty
        slugged_name = item['title'].replace(" ", "-")
        slugged_name = slugged_name.replace("(", "")
        slugged_name = slugged_name.replace(")", "")
        slugged_name = slugged_name.replace("/", "-")
        project_name = item['project_name']
        # nicely formatted, woop woop
        with open(f'./rekts/{slugged_name}.json', 'w') as rekt:
            json.dump(item, rekt, indent=4)

        markdownTitle = f"# {project_name}"
        markdownLink = f"[{project_name}]({item['website_link']})"
        formatted_funds_lost = "${:,.2f}".format(item['funds_lost'])
        formatted_returned = "${:,.2f}".format(item['funds_returned'])
        markdownAmountLost = f"Amount Lost: {formatted_funds_lost}"
        markdownFundsReturned = f"Funds Returned: {formatted_returned}"
        markdownCategory = f"Category: {item['name_categories']}"
        markdownDate = f"Date: {item['date']}"
        markdownscamNetworks = f"Network: {item['scamNetworks'][0]['networks']['name']}"
        markdownLogoFromRepo = f"/rektimages/{slugged_name}.png"
        markdownImage = f"![{project_name}]({markdownLogoFromRepo})"
        markdownDescription = convert_html_to_markdown(item['description'])
        markdownFullWithScamNetworks = f"{markdownTitle}\n{markdownImage}\n- {markdownAmountLost}\n- {markdownFundsReturned}\n- {markdownCategory}\n- {markdownDate}\n- {markdownscamNetworks}\n\n"
        linkToMarkdownFile = f'/rekts/{slugged_name}.md'
        markdownFullwithLinkToLearnMore = f"{markdownFullWithScamNetworks}\n[Learn More]({linkToMarkdownFile})\n\n"
        markdownFullWithDescription = f"{markdownTitle}\n{markdownImage}\n- {markdownAmountLost}\n- {markdownFundsReturned}\n- {markdownCategory}\n- {markdownDate}\n\n{markdownDescription}\n\n"            
        # lol, I probs don't need all these variables but whatever

        proof_link = item['proof_link']
        if proof_link is not None:
            proof_link_array = proof_link.split(",")
            links = ""
            for link in proof_link_array:
                links += f"- [{link}]({link})\n"
            markdownFullWithDescription += f"Proof Links:\n{links}\n"

        # might be a better way to do this
        urllib.request.urlretrieve(markdownLogo, f"rektimages/{slugged_name}.png")

        with open(f'./rekts/{slugged_name}.md', 'w') as rekt:
            rekt.write(markdownFullWithDescription + '\n')
        
        commandToRun = f"git add * && git commit -m 'add {project_name} to rekts'"
        returned_value = subprocess.call(commandToRun, shell=True)  # returns the exit code in unix

def convert_html_to_markdown(html):
    if html is None:
        return ""

    text_maker = html2text.HTML2Text()
    text_maker.body_width = 0  # This sets the body width to unlimited which helps in not wrapping the text automatically.
    markdown_content = text_maker.handle(html)

    return markdown_content

def make_toc(items, filename):
    tocsWithTitle = "# Table of Contents\n\n"
    for item in items:
        project_name = item['title']
        formatted_funds_lost = "${:,.2f}".format(item['funds_lost'])
        formatted_returned = "${:,.2f}".format(item['funds_returned'])
        slugged_name = project_name.replace(" ", "-")
        slugged_name = slugged_name.replace("(", "")
        slugged_name = slugged_name.replace(")", "")
        slugged_name = slugged_name.replace("/", "-")
        linkToMarkdownFile = f'/rekts/{slugged_name}.md'
        tocsWithTitle += f"- [{project_name}]({linkToMarkdownFile}) - Lost: {formatted_funds_lost} Recovered: {formatted_returned} \n"
    with open(filename, 'w') as readme:
        readme.write(tocsWithTitle + '\n')

def make_title(filename):
    title = "# Rekt Projects\n\n"
    with open(filename, 'w') as readme:
        readme.write(title + '\n')
                
def do_the_do():
    with open('rektdb.json', 'r') as f:
        data = json.load(f)
        items = data['items']
        # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # readme_file_name = f'README.md'
        # add_title = f"# Rekt Projects\n\n"
        # make_toc(items, readme_file_name)
        # rekt_loop(items, 3397)
        # add up all the funds lost
        total_funds_lost = 0
        for item in items:
            formatted_funds_lost = "${:,.2f}".format(item['funds_lost'])
            total_funds_lost += item['funds_lost']
        
        formatted_total_funds_lost = "${:,.2f}".format(total_funds_lost)

        print(f"Total Funds Lost: {formatted_total_funds_lost}")


do_the_do()