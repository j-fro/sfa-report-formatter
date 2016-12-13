import pandas as pd
import openpyxl
import yaml

def formatter(path, settings):
    book = openpyxl.load_workbook(path)
    sheet = book.active
    print ("Formatting data.")
    for num in range(settings['First Store Column'], settings['Last Column']):
        sheet.cell(row=settings['Type Row'], column=num).value += (
            "," + sheet.cell(row=settings['Store Row'], column=(
                num - settings['First Store Column']) // settings['Number of Types']
                * settings['Number of Types'] + settings['First Store Column']).value
        )
    print ("Combining index columns")
    for index in settings["Index Columns"]:
        #sheet.unmerge_cells(start_row=settings["Type Row"] - 2, start_column=index + 1,
        #                    end_row=settings["Type Row"] - 2, end_column=index + 1)
        sheet.cell(row=settings["Type Row"], column=index + 1).value = (
            sheet.cell(row=settings["Type Row"] + 2, column=index + 1).value
        )
    #sheet.unmerge_cells(start_row=settings["Type Row"], start_column=settings["Style Column"] - 1,
    #                    end_row=settings["Type Row"], end_column=settings["Style Column"])
    sheet.cell(row=settings["Type Row"], column=settings["Style Column"]).value = (
        sheet.cell(row=settings["Type Row"], column=settings["Style Column"] - 1).value
    )
    return book

def stacker(path, settings):
    print("Stacking data")
    report = pd.read_excel(
        path,
        sheetname=settings["Sheet Name"],
        header=settings["Type Row"] - 1,
        index_col=settings["Index Columns"]
    )
    return report.stack()

def output(report, path):
    print ("Saving workbook to " + path)
    report.to_frame(name="Values").to_csv(path)

def format_file(inbound_path, settings_path, outbound_path):
    print ("Getting settings")
    with open(settings_path) as file:
        settings = yaml.load(file)
    book = formatter(inbound_path, settings)
    book.save("Intermediate.xlsx")
    output(stacker("Intermediate.xlsx", settings), outbound_path)

if __name__ == '__main__':
    # print "Getting settings."
    with open("Settings.yml") as file:
        settings = yaml.load(file)
    # print "Reading workbook. This may take a few minutes."
    book = formatter("Marco Bicego Style by Store Selling Week November Week 1.xlsx", settings)
    book.save("Test.xlsx")
    # print "Reshaping workbook"
    output(stacker("Test.xlsx", settings), "Test2.csv")
    # print "Output complete."
