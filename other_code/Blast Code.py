from selenium import webdriver
import openpyxl
from openpyxl.styles import Font
from openpyxl.styles.colors import BLUE


f = open("Accession_Numbers.txt", "r")
accessionNumbers = []
reverseAccessionNumbers = []
for line in f.readlines():
    accessionNumbers.append(line[0:len(line)-1])
workbookName = 'firstBlast10.xlsx'
wb = openpyxl.Workbook()
sheets = []
driver = webdriver.Chrome()
accessionNumbers = ["YP_009160396.1", "YP_009160331.1"] #use to test code quickly without searching
def main():
    for i in range(len(accessionNumbers)):
        dataLists = databaseSearch(accessionNumbers[i], "Bacteria (taxid:2)")
        excelUpdate(dataLists, "Forward", i)
    for i in range(len(reverseAccessionNumbers)):
        dataLists = databaseSearch(reverseAccessionNumbers[i], "Viruses (taxid:10239)")
        excelUpdate(dataLists, "Backward", i)
    wb.remove_sheet(sheets[0])
    print ("done")
    driver.close()
def databaseSearch(accessionNumber, organismCriteria):
    driver.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins")
    query_box = driver.find_element_by_name('QUERY')
    query_box.send_keys(accessionNumber)
    organism_box = driver.find_element_by_name("EQ_MENU")
    organism_box.send_keys(organismCriteria)
    blast_button = driver.find_element_by_id('b1')
    blast_button.click()
    confirmation = ""
    while confirmation == "":
        try:
            confirmation = driver.find_element_by_id('smrtBlastFullSearch')
        except:
            pass
    descriptionsList = driver.find_elements_by_class_name("deflnDesc")
    maxScoreList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c3']")
    totalScoreList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c4']")
    queryCoverList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c5']")
    eValuesList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c6']")
    perIndList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c7']")
    accessionList = driver.find_elements_by_xpath("//table[@id='dscTable']//tr//td[@class='c1 l lim']")
    infoLists = [descriptionsList, maxScoreList, totalScoreList, queryCoverList, eValuesList, perIndList, accessionList]
    for i in range(len(infoLists)):
        infoLists[i] = infoLists[i][0:10]
        for c in range(len(infoLists[i])):
            infoLists[i][c] = infoLists[i][c].text
            try:
                infoLists[i][c] = float(infoLists[i][c])
            except ValueError:
                pass
    if organismCriteria == "Bacteria (taxid:2)":
        wb.create_sheet(title=accessionNumber)
        sheets.append(wb.get_sheet_by_name(accessionNumber))
        reverseAccessionNumbers.append(infoLists[6][0])
    wb.save(workbookName)
    return (infoLists)
def textWithFont(sheet, locations, text, bolded = False, colors = "FF000000"):
    for location in locations:
        sheet[location] = text
        sheet[location].font = Font(bold = bolded, color = colors)
def excelUpdate(infoLists, direction, sheetNumber):
    textWithFont(sheets[sheetNumber], ["A1"], "Forward Blast", bolded = True)
    textWithFont(sheets[sheetNumber], ["A14"], "Reverse Blast", bolded = True)
    textWithFont(sheets[sheetNumber], ["A2", "A15"], "Description", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["B2", "B15"], "Max Score", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["C2", "C15"], "Total Score", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["D2", "D15"], "Query Cover", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["E2", "E15"], "E value", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["F2", "F15"], "Per. Ident", bolded = True, colors = BLUE)
    textWithFont(sheets[sheetNumber], ["G2", "G15"], "Accession", bolded = True, colors = BLUE)
    indexToLetter = {0 : "A", 1 : "B", 2 : "C", 3 : "D", 4 : "E", 5 : "F", 6 : "G"}
    startingRow = 3 if direction == "Forward" else 16
    for c in range(len(infoLists)):
        for r in range(len(infoLists[c])):
            row = startingRow + r
            sheets[sheetNumber][indexToLetter[c] + str(row)] = infoLists[c][r]
            wb.save(workbookName)
main()
