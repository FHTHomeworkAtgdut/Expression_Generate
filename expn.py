# coding=gb2312
import random
from fractions import Fraction
import argparse
import sys
operator_list = ['+', '-', '*', '/']
max_num = 10
expression_num = 10000
max_depth = 2
expression_tree_list  = []
expression_list = []
answer_list = []
text_path = ""
answer_path = ""

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def generate_num():
    if random.random() < 0.75:
        return  random.randint(1, max_num)
    else:
        # return str(random.randint(1, max_num))+'/'+(str(random.randint(1, max_num)))
        return Fraction(random.randint(1, max_num),random.randint(1, max_num))

def generate_expression(depth):
    if depth == 0 or random.random() < 0.3 and depth != max_depth:
        # 当达到指定深度时， 避免出现 x = x 的情况
        num = generate_num()
        return TreeNode(num)
    else:
        operator = random.choice(operator_list)
        node = TreeNode(operator)
        node.left = generate_expression(depth - 1)
        node.right = generate_expression(depth - 1)
        if type(node.left.val) != str and type(node.right.val)!= str:
            if node.left.val - node.right.val <= 0 and node.val == '-':
                while node.left.val - node.right.val <= 0:
                    node.left.val = generate_num()
                    node.right.val = generate_num()
        return node


def is_repeated(p,q):
    if p == q:
        return True
    if p.val == q.val:
        return (is_repeated(p.left,q.left) and is_repeated(p.right,q.right)) or (is_repeated(p.right,q.left) and is_repeated(p.left,q.right))
    else:
        return False;

def expression_string(root,root_bracket): # 整条式子外部不需要括号
    if root is None:
        return ""

    if root.left is None and root.right is None:
        return str(root.val)
    else:
    
        left_expr = expression_string(root.left,root_bracket)
        right_expr = expression_string(root.right,root_bracket)
        operator = root.val

        if operator in "+-" and root_bracket != root:
            return f"({left_expr} {operator} {right_expr})"
        else:
            return f"{left_expr} {operator} {right_expr}"


def calculate_expression(root):
    if root is None:
        return Fraction(0)

    if root.left is None and root.right is None:
        return root.val
    else:
        left_value = calculate_expression(root.left)
        right_value = calculate_expression(root.right)
        operator = root.val

        if operator == '+':
            return left_value + right_value
        elif operator == '-':
            return left_value - right_value
        elif operator == '*':
            return left_value * right_value
        elif operator == '/':
            return Fraction(left_value,right_value)


def add_to_list(expression_tree,ans):
    if ans<0: # 避免结果为负数
        return False
    if len(expression_list) == 0:
        expression = expression_string(expression_tree,expression_tree)
        expression_tree_list.append(expression_tree)
        expression_list.append(expression)
        answer_list.append(ans)
        return True
    else:
        for i in range(len(expression_tree_list)):
            if(is_repeated(expression_tree,expression_tree_list[i]) == True):
                return False
        expression = expression_string(expression_tree,expression_tree)
        expression_tree_list.append(expression_tree)
        expression_list.append(expression)
        answer_list.append(ans)
        return True

def create_expression():
    while len(expression_list) < expression_num:
            expression = generate_expression(max_depth)
            # expression_string(expression_tree,expression_tree)+" = "+str(calculate_expression(expression_tree))
            ans = calculate_expression(expression)
            add_to_list(expression,ans)              
    save_to_txt(expression_list,"expression.txt")
    save_to_txt(answer_list,"answer.txt")



def save_to_txt(list,path):
    f = open(path,"w")
    
    i = 0
    for line in list:
        f.write(str(i)+". "+str(line) + '\n')
        i = i+1
    f.close()


def correct_answer(answer_path,test_path):
    f_ans = open(answer_path,"r")
    f_test = open(test_path,"r")
    right_list = []
    wrong_list = []
    # lines_ans = f_ans.readline()
    # lines_test = f_test.readline()
    i = 1
    while True:
        lines_ans = f_ans.readline().strip()
        lines_test = f_test.readline().strip()
        if lines_ans and lines_test:
            if lines_ans != lines_test:
                wrong_list.append(i)
                i = i + 1
            else:
                right_list.append(i)
                i = i + 1
        else:
            break
    f_ans.close()
    f_test.close()
    f=open("Grade.txt","w")
    f.write("Correct  "+str(len(right_list))+"     "+str(right_list))
    f.write("\n")
    f.write("Wrong  "+str(len(wrong_list))+"     "  +str(wrong_list))
    print("Correct  "+str(len(right_list))+"     "+str(right_list))
    print("Wrong  "+str(len(wrong_list))+"     "  +str(wrong_list))
    f.close()
    

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-r',"--range", type=int,default=10)
        parser.add_argument('-n',"--num" ,type=int,default=1000)
        parser.add_argument('-e',"--exercise", type=str,default="exercise.txt")
        parser.add_argument('-a',"--answer", type=str,default="answer.txt")
        args = parser.parse_args()
        
        
        
        if True:
            global max_num,expression_num
            max_num = args.range
            expression_num = args.num
            create_expression()
        else:
            answer_path = args.answer
            text_path =  args.exercise
            correct_answer(answer_path,text_path)
    
    
if __name__ == "__main__":
    main()
