 #Hakukone

while True:
	print("Exit: q and enter")
	haku = input("Write your query here: ")
	if quit == "q" or quit  == "Q":
		break
				

try:

    text_file = open("enwiki.txt", "r")

    list_of_articles = []

    for line in text_file:

        if "<article name=" in line:

            text = ""

            continue

        elif "</article>" in line:

            list_of_articles.append(text)

        else:

            line = line.strip()

            text += " " + line

except OSError:

    print("File not found")

print(list_of_articles[:2])
