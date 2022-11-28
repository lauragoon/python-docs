import re

from docgen import generate_fxn_html, generate_init_html, generate_end_html
from enums import FunctionAttrs


def init_fxn_info_dict():
    return {
        FunctionAttrs.NAME.value: None,
        FunctionAttrs.PARAM_NAMES.value: [],
        FunctionAttrs.PARAM_OPTIONAL_VALS.value: {},
        FunctionAttrs.DESC.value: "",
        FunctionAttrs.RETURN_TYPE.value: None,
        FunctionAttrs.RETURN_DESC.value: "",
        FunctionAttrs.PARAM_DESC.value: {} # { param : [type, desc] }
    }

def process_file(filename):
    processed_fxn = []
    
    with open(filename) as fp:
        line_num = 0
        at_doc_comment = False
        curr_fxn = init_fxn_info_dict()
        
        # iterate through file
        for line in fp:
            line_num += 1
            stripped_line = line.strip()
            
            # fxn declaration
            if stripped_line[0:3] == "def":
                
                # clear vars for new fxn info
                if curr_fxn[FunctionAttrs.NAME.value] is not None:
                    processed_fxn.append(curr_fxn)
                curr_fxn = init_fxn_info_dict()
                
                line_delimed = re.split(r"\s|\(|\)|,|:", stripped_line)
                line_delimed = list(filter(None, line_delimed)) # remove empty strings from regex split
                
                curr_fxn[FunctionAttrs.NAME.value] = line_delimed[1]
                
                param_declarations = line_delimed[2:]
                for param in param_declarations:
                    if "=" in param:
                        param_delimed = re.split(r'=|\"+', param)
                        param_delimed = list(filter(None, param_delimed))
                        curr_fxn[FunctionAttrs.PARAM_OPTIONAL_VALS.value][param_delimed[0]] = param_delimed[1]
                        curr_fxn[FunctionAttrs.PARAM_NAMES.value].append(param_delimed[0])
                    else:
                        curr_fxn[FunctionAttrs.PARAM_NAMES.value].append(param)
              
            # beginning or end of python doc comment  
            elif stripped_line[0:3] == '"""':
                at_doc_comment = not at_doc_comment
                
            # python doc comment
            elif len(stripped_line) > 0 and at_doc_comment:
                
                if stripped_line.split(" ")[0] not in curr_fxn[FunctionAttrs.PARAM_NAMES.value]:
                    
                    # return desc
                    if stripped_line[0:8] == "Returns:":
                        return_desc_delimed = re.split(r"\[|\]|\s", stripped_line[8:], 4)
                        return_desc_delimed = list(filter(None, return_desc_delimed))
                        
                        curr_fxn[FunctionAttrs.RETURN_TYPE.value] = return_desc_delimed[0]
                        curr_fxn[FunctionAttrs.RETURN_DESC.value] = return_desc_delimed[1] if len(return_desc_delimed) > 1 else ""
                        
                    # python doc comment desc
                    else:
                        if len(curr_fxn[FunctionAttrs.DESC.value]) > 0:
                            curr_fxn[FunctionAttrs.DESC.value] += "\n"
                        curr_fxn[FunctionAttrs.DESC.value] += stripped_line
                        
                # param desc
                else:
                    param_desc_delimed = re.split(r"\s|[|]|:", stripped_line, 4)
                    param_desc_delimed = list(filter(None, param_desc_delimed))
                    
                    param_name = param_desc_delimed[0]
                    
                    param_attr = re.split(r"\[|\]", param_desc_delimed[1])
                    param_attr = list(filter(None, param_attr))
                    if "optional" in param_attr and param_name not in curr_fxn[FunctionAttrs.PARAM_OPTIONAL_VALS.value].keys():
                        print("process_file ERROR: Optional parameter not properly defined.", file=sys.stderr)
                    if len(param_attr) > 2:
                        print("process_file ERROR: More param attributes defined than necessary.", file=sys.stderr)
                    
                    param_desc = param_desc_delimed[2]
                    
                    curr_fxn[FunctionAttrs.PARAM_DESC.value][param_name] = [param_attr[0], param_desc]
                    
        processed_fxn.append(curr_fxn)
        
    return processed_fxn

def generate_html(processed_output):
    f = open("test.html", "w")
    
    f.write(generate_init_html())
    
    for fxn in processed_output:
        f.write(generate_fxn_html(fxn))
    
    f.write(generate_end_html())
    
    f.close()

def main():
    processed_output = process_file("fxn.py")
    generate_html(processed_output)

main()
