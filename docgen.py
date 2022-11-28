from enums import FunctionAttrs

def generate_fxn_html(fxn_dict):
    ret_html = "<h1>"
    ret_html += fxn_dict[FunctionAttrs.NAME.value]
    ret_html += "</h1>\n"
    
    fxn_declaration = fxn_dict[FunctionAttrs.NAME.value]
    fxn_declaration += "("
    for fxn_param in fxn_dict[FunctionAttrs.PARAM_NAMES.value]:
        fxn_declaration += fxn_param
        if fxn_param in fxn_dict[FunctionAttrs.PARAM_OPTIONAL_VALS.value].keys():
            fxn_declaration += '="' + fxn_dict[FunctionAttrs.PARAM_OPTIONAL_VALS.value][fxn_param] + '"'
        fxn_declaration += ","
    fxn_declaration = fxn_declaration[0:-1] + ")"
    
    ret_html += "<h2>" + fxn_declaration + "</h2>\n"
    ret_html += "<p>" + fxn_dict[FunctionAttrs.DESC.value] + "</p>\n"
    ret_html += "<h3>Returns:</h3>"
    ret_html += "<b>" + fxn_dict[FunctionAttrs.RETURN_TYPE.value] + "</b> <span>" + \
                fxn_dict[FunctionAttrs.RETURN_DESC.value] + "</span>"
    ret_html += "<h3>Parameter(s):</h3>\n"
    
    ret_html += "<table><tr>\n" + \
                "<th>Name</th>\n" + \
                "<th>Type</th>\n" + \
                "<th>Description</th>\n</tr>\n"
    for fxn_param in fxn_dict[FunctionAttrs.PARAM_NAMES.value]:
        param_info = fxn_dict[FunctionAttrs.PARAM_DESC.value][fxn_param]
        ret_html += "<tr>\n"
        ret_html += "<th>"
        if fxn_param in fxn_dict[FunctionAttrs.PARAM_OPTIONAL_VALS.value].keys():
            ret_html += "<i>" + fxn_param + "</i>"
        else:
            ret_html += fxn_param
        ret_html += "</th><th>" + param_info[0] + "</th><th>" + param_info[1] + "</th>"
        ret_html += "</tr>\n"
    
    ret_html += "</table>\n"
    
    return ret_html
               
def generate_init_html():
    return "<!DOCTYPE html>\n" + \
            '<html lang="en">\n' + \
            "<head>\n" + \
            '    <meta charset="utf-8">\n' + \
            "    <title>PythonDocs</title>\n" + \
            '    <link href="style.css" rel="stylesheet" />' + \
            "</head>\n" + \
            "<body>\n"
            
def generate_end_html():
    return "</body>\n</html>"
