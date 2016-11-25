#coding=utf-8
class jParser(object):
    def __init__(self, text, items):
        self.text = text
        self.items = items
    
    def parse(self):
        # Get text
        tempText = self.text
        # Initialize values
        isCode = False
        code = ""
        output = ""
        pointer = 0
        length = len(tempText)
        tempText += " "# To avoid data overflow.
        while True:
            # Common text
            if not isCode and tempText[pointer] != "{" and tempText[pointer+1] != "{" :
                output += tempText[pointer]
            # Code begin
            elif tempText[pointer] == "{" and tempText[pointer+1] == "{":
                pointer += 1
                isCode = True
                code = ""
            # Code end
            elif isCode and tempText[pointer] == "}" and tempText[pointer+1] == "}":
                pointer += 1
                isCode = False
                # Parse code (return operations)
                operation = []
                operation = self.codeParser(code)
                # Get command
                command = operation["command"]
                # Solve command
                # Command common
                if command == "Common":
                    try:
                        output += operation.get("detail")
                    except:
                        pass
                # Command default
                elif command == "Error":
                    pass
            elif isCode:
                code += tempText[pointer]
        
            pointer += 1
            if pointer == length:
                break
        return output
    
    def codeParser(self, code):
        # Initialize return data
        result = {}
        # Split source data
        data = code.split()
        # Case for
        if data[0] == "for" and data[2] == "to":
            pass
        # Case if
        elif data[0] == "if":
            pass
        # Case common ( All data are printed as value ).
        elif data[0][0] == "$":
            # Check if each data is legal.
            for d in data:
                if d[0] != "$":
                    # If is illegal, return ERROR.
                    result["command"] = "Error"
                    return result
            result["command"] = "Common"
            # Reset or announce detail
            detail = []
            # Get values
            for d in data:
                detail.append(self.items.get(d.replace("$", "")))
            try:
                result["detail"] = " ".join(detail)
            # If the list have only one item, join will return an error. 
            except:
                result["detail"] = detail[0]
            return result
        # Case default
        else:
            result["command"] = "Error"
            return result