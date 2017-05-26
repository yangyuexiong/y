
def add_node(tree_dic,comment):
    if comment.parent_comment is None:
        #判断父级是否None，是：生成在此层。
        tree_dic[comment] = {}
    else:#循环当前整个字典直到找到
        for k,v in tree_dic.items():
            if k == comment.parent_comment:#找到父级
                tree_dic[comment.parent_comment][comment]={}#增加
            else: #进入下一层循环继续寻找
                add_node(v,comment)



def render_tree_node(tree_dic,margin_val):
    html = ""
    for k,v in tree_dic.items():
        ele ="<div class='caomment-node' style='margin-left: %spx'>" % margin_val + k.comment + "</div>"
        html += ele
        render_tree_node(v,margin_val+10)
    return html


def render_comment_tree(tree_dic):
    html = ""
    for k,v in tree_dic.items():
        ele = "<div class='root-comment'>" + k.comment + "<span style='margin-left:20px'> %s </span>"%k.date \
              + "<span style='margin-left:20px'>%s</span>" %k.user.name + "</div>"
        html += ele
        html += render_tree_node(v,0)
    return html


def build_tree(comment_set):
    #print(comment_set)
    terr_dic = {}
    for comment in comment_set:
        add_node(terr_dic,comment)

    print("-")
    for k,v in terr_dic.items():
        print(k,v)
    return(terr_dic)