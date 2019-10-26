from TextSummary import TextSummary as ts

location = "doc.txt"
with open(location, "r") as file:
    doc = file.read().replace("\n", "")

ts = ts(doc)
print(ts.summarize(threshold=0.6))
