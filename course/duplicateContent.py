from .models import Course, Lesson,ItemList
from .serializers import CourseSerializer, LessonSerializer
from word_card.models import WordCard
from word_card.serializers import WordCardSerializer
from dialogue.models import DialogueGroup,Dialogue,TestAnswer,TestCard,Ballon,ImageModal
from dialogue.serializers   import DialogueGroupSerializer
from alerts.models import Note,Popup,Label
from alerts.serializers import NoteSerializer,PopupSerializer,LabelSerializer


def duplicateCourse(old_id,new_id):
    # step 1 : retrieve all stuffs related to course with old_id and
    # then store their id's and model names in a linked list.
    course = Course.objects.filter(id=old_id).first()
    duplicateLessons(new_id,course)
    #  step 2 : take the linked list and duplicate everything with same level
    #  of depth and save new id's in a same type linked list.
    return True

def duplicateLessons(new_id,course_object):
    all_lessons = Lesson.objects.filter(parent_course=course_object)
    new_course = Course.objects.filter(id=new_id).first()
    for object_ in all_lessons:
        new_lesson = Lesson.objects.create(
            parent_course=new_course,
            title=object_.title,
            author=object_.author,
            info_type=object_.info_type
        )
        new_lesson.save()
        duplicateDialogueGrp(object_,new_lesson)
        duplicateWordCards(object_,new_lesson)
    return True



def duplicateWordCards(o_l,n_l):
    all_Word_cards = WordCard.objects.filter(lesson=o_l)
    for wc in all_Word_cards:
        new_WC = WordCard.objects.create(
            word=wc.word,
            author=wc.author,
            dictionary=wc.dictionary,
            lesson=n_l,
            linked=wc.linked,
            info_type=wc.info_type
            # popup_linked=
            # note_linked
            # label_linked
        )
        new_WC.save()
        new_popups = duplicate_popups(o_l,n_l)
        for pop in new_popups:
            new_WC.popup_linked.add(pop)
            
        new_note_linked = duplicate_note_linked(o_l,n_l)
        for pop in new_note_linked:
            new_WC.note_linked.add(pop)
        new_label = duplicate_label(o_l,n_l)
        for nl in new_label:
            new_WC.label_linked.add(nl)
        new_WC.save()
    return True
def duplicate_popups(ol,nl):
    out=[]
    all_p = Popup.objects.filter(lesson=ol)
    for p in all_p:
        new_p = Popup.objects.create(
            title=p.title,
            file=p.file,
            text=p.text,
            lesson=nl,
            info_type=p.info_type
        )
        new_p.save()
        out.append(new_p.id)
    return out
def duplicate_note_linked(ol,nl):
    all_nl = Note.objects.filter(lesson=ol)
    out=[]
    for p in all_nl:
        new_p = Note.objects.create(
            title=p.title,
            file=p.file,
            text=p.text,
            lesson=nl,
            info_type=p.info_type,
            subtitle=p.subtitle
        )
        new_p.save()
        out.append(new_p.id)

    return out
def duplicate_label(ol,nl):
    out=[]
    all_nl = Label.objects.filter(lesson=ol)
    for p in all_nl:
        new_p = Label.objects.create(
            title=p.title,
            lesson=nl,
            info_type=p.info_type,
        )
        new_p.save()
        out.append(new_p.id)
    return out


def duplicateDialogueGrp(old_object,new_object):
    all_dg = DialogueGroup.objects.filter(lesson=old_object)
    for object_ in all_dg:
        new_dg = DialogueGroup.objects.create(
            user=object_.user,
            lesson=new_object,
            title=object_.title,
            info_type=object_.info_type
        )
        new_dg.save()
        duplicateDialogue(object_,new_object,new_dg)
    return True

def duplicateDialogue(old_dg,new_lesson,new_dg):
    all_d = Dialogue.objects.filter(dialogue_group=old_dg,)
    for object_ in all_d:
        new_d = Dialogue.objects.create(
        user=object_.user,
        lesson=new_lesson,
        dialogue_group=new_dg,
        title=object_.title,
        )
        all_ballons= object_.ballon.all()
        all_image = object_.image.all()
        for i in all_ballons:
            new_id = duplicateBallon(i.id)
            new_d.ballon.add(new_id)
        for j in all_image:
            new_i_id = duplicateImage(j.id)
            new_d.image.add(new_i_id)
        new_d.save()
        all_tests = TestCard.objects.filter(dialogue=object_)
        for test in all_tests:
            new_test = TestCard.objects.create(
                dialogue_group=new_dg,
                dialogue=new_d,
                card_type=test.card_type,
                user=test.user,
                test_text=test.test_text,
                hide=test.hide
            )
            new_test.save()
            new_answers = duplicateTestAnswers(test,new_test)
            for answer in new_answers:
                new_test.answers.add(answer)
            new_test.save()
    return True

def duplicateTestAnswers(old,new):
    all_answers = TestAnswer.objects.filter(test=old)
    out=[]
    for answer in all_answers:
        new_a = TestAnswer.objects.create(
            text=answer.text,
            test=new,
            answer_type=answer.answer_type,
            user=answer.user,
            info_type=answer.info_type
        )
        new_a.save()
        out.append(new_a.id)
    return out
def duplicateBallon(i):
    ob = Ballon.objects.filter(id=i).first()
    new_bal = Ballon.objects.create(
        avatar=ob.avatar,
        file=ob.file,
        meaning=ob.meaning,
        ideogram=ob.ideogram,
        pronunciation=ob.pronunciation,
        user=ob.user,
        info_type=ob.info_type
    )
    new_bal.save()
    return new_bal.id
def duplicateImage(i):
    ob = ImageModal.objects.filter(id=i).first()
    new_img = ImageModal.objects.create(
        file=ob.file,
        user=ob.user,
        info_type=ob.info_type,
        hints=ob.hints
    )
    new_img.save()
    return new_img.id
