import re

NAME = "name"
PARAM_NAMES = "param_names"
PARAM_OPTIONAL_VALS = "param_optional_vals"
DESC = "desc"
RETURN_TYPE = "return_type"
RETURN_DESC = "return_desc"
PARAM_DESC = "param_desc"

def init_fxn_info_dict():
    return {
        NAME: None,
        PARAM_NAMES: [],
        PARAM_OPTIONAL_VALS: {},
        DESC: "",
        RETURN_TYPE: None,
        RETURN_DESC: "",
        PARAM_DESC: {} # { param : [type, desc] }
    }

def process_file(filename):
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
                curr_fxn = init_fxn_info_dict()
                
                line_delimed = re.split(r"\s|\(|\)|,|:", stripped_line)
                line_delimed = list(filter(None, line_delimed)) # remove empty strings from regex split
                
                curr_fxn[NAME] = line_delimed[1]
                
                param_declarations = line_delimed[2:]
                for param in param_declarations:
                    if "=" in param:
                        param_delimed = re.split(r'=|\"+', param)
                        param_delimed = list(filter(None, param_delimed))
                        curr_fxn[PARAM_OPTIONAL_VALS][param_delimed[0]] = param_delimed[1]
                        curr_fxn[PARAM_NAMES].append(param_delimed[0])
                    else:
                        curr_fxn[PARAM_NAMES].append(param)
              
            # beginning or end of python doc comment  
            elif stripped_line[0:3] == '"""':
                at_doc_comment = not at_doc_comment
                
            # python doc comment
            elif len(stripped_line) > 0 and at_doc_comment:
                
                if stripped_line.split(" ")[0] not in curr_fxn[PARAM_NAMES]:
                    
                    # return desc
                    if stripped_line[0:8] == "Returns:":
                        return_desc_delimed = re.split(r"\[|\]|\s", stripped_line[8:], 4)
                        return_desc_delimed = list(filter(None, return_desc_delimed))
                        
                        curr_fxn[RETURN_TYPE] = return_desc_delimed[0]
                        curr_fxn[RETURN_DESC] = return_desc_delimed[1] if len(return_desc_delimed) > 1 else ""
                        
                    # python doc comment desc
                    else:
                        if len(curr_fxn[DESC]) > 0:
                            curr_fxn[DESC] += "\n"
                        curr_fxn[DESC] += stripped_line
                        
                # param desc
                else:
                    param_desc_delimed = re.split(r"\s|[|]|:", stripped_line, 4)
                    param_desc_delimed = list(filter(None, param_desc_delimed))
                    
                    param_name = param_desc_delimed[0]
                    
                    param_attr = re.split(r"\[|\]", param_desc_delimed[1])
                    param_attr = list(filter(None, param_attr))
                    if "optional" in param_attr and param_name not in curr_fxn[PARAM_OPTIONAL_VALS].keys():
                        print("process_file ERROR: Optional parameter not properly defined.", file=sys.stderr)
                    if len(param_attr) > 2:
                        print("process_file ERROR: More param attributes defined than necessary.", file=sys.stderr)
                    
                    param_desc = param_desc_delimed[2]
                    
                    curr_fxn[PARAM_DESC][param_name] = [param_attr[0], param_desc]
                

def main():
    process_file("fxn.py")


main()
