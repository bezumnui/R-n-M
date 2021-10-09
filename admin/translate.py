
def prefix_translate(ctx, p, part): #p - prefix
    if part == 0:
        return [f"Usage: {p}prefix {{prefix}}", f"Использование: {p}prefix {{префикс}}"]
    if part == 1:
        return ["Prefix was successful changed to **{}**", "Префикс успешно изменен на: **{}**"]

def languages_translate(p, part): #p - prefix
    if part == 0:
        return [f"Usage: {p}lan {{language}}", f"Использование: {p}lan {{language}}"]
    if part == 1:
        return [f"Languages: ", f"Языки: "]
    if part == 2:
        return [
            "en - English",
            "ru - Русский"
        ]
    if part == 3:
        return ["Language was changed successful!", "Язык был успешно изменен!"]

def clear_translate(part, c=0):
    if part == 0:
        return [f"Was deleted: {c} messages", f"Было удалено: {c} сообщений"]
    if part == 1:
        return ["Was deleted: {0}/{1}\n{2}%", "Было удалено: {0}/{1}\n{2}%"]
def RRA_translate(part=0, p=""):
    if part == 0:
        return [f"! - must be \n\nUsage:\n {p}RRAdd *!message_id !emoji !role*  [+(default)/-]",
                f"! - обязательно \n\nИспользование:\n {p}RRAdd *!айди_сообщения !эмоджи !роль*  [+(по ум.)/-]",]

def RRR_translate(part=0, p=""):
    if part == 0:
        return [f"Usage:\n {p}RRRemove *message_id emoji*",
                f"Использование:\n {p}RRRemove *айди_сообщения эмоджи*",]

def RRD_translate(part=0, p=""):
    if part == 0:
        return [f"Usage:\n {p}RRDelete *message_id*",
                f"Использование:\n {p}RRDelete *айди_сообщения*",]

kick_ussage = ["Usage:\n {}kick @member (reason)",
               "Использование:\n {}kick @учасник (причина)"]

ban_ussage = ["Usage:\n {}ban @member (reason)",
               "Использование:\n {}ban @учасник (причина)"]