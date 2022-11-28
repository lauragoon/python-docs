from enums import FunctionAttrs

def generate_fxn_html(fxn_dict):
    ret_html = "<h1>"
    ret_html += fxn_dict[FunctionAttrs.NAME.value]
    ret_html += "</h1><h2>Parameters:</h2>"
    
    return ret_html
               
def generate_init_html():
    return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <title></title>
               <link href="style.css" rel="stylesheet" />
            </head>
            <body>
            """
            
def generate_end_html():
    return """
            </body>
            </html>
            """
