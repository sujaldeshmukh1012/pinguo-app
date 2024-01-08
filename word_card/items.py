from course.models import ItemList,Lesson
# from course.objects import giveMeObject




def itemAddition(type,lesson,id):
    l = Lesson.objects.filter(id=lesson).first()
    item,created = ItemList.objects.get_or_create(type=type,lesson=l,item_id=id)
    # if(type == "word_card"):
    #     w = giveMeObject("word_card",id)
    #     item.wc_object = w
    # elif(type == "dialogue_group"):
    #     d = giveMeObject("dialogue_group",id)
    #     item.dg_object = d
    # elif(type == "label"):
    #     l = giveMeObject("label",id)
    #     item.l_object = l
    # elif(type == "note"):
    #     n = giveMeObject("note",id)
    #     item.n_object = n
    # elif(type == "popup"):
    #     p = giveMeObject("popup",id)
    #     item.pu_object = p
    # else:
    #     pass
    print("itemAddition called===========")
    item.save()
    return True

def itemRomoval(type,lesson,id):
    l = Lesson.objects.filter(id=lesson).first()
    item = ItemList.objects.get(type=type,lesson=l,item_id=id)
    item.delete()
    return True

