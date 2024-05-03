def main():
    scifi_authors = [
        "Isaac Asimov","Ray Bradbury","Robert Heinlein","Arthus C. Clarke","Frank Herbert","Orson Scott Card","Douglas Adams","H. G. Wells","Leigh Brackett"
    ]
    print(scifi_authors)
    scifi_authors.sort(key=lambda name: name.split(" ")[-1])
    print(scifi_authors)
if __name__ == "__main__":
    main()
