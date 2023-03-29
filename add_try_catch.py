from base_operator import BaseOperator
import random
import math


class AddTryCatch(BaseOperator):
    def __init__(self, language: str):
        super(AddTryCatch, self).__init__(language)

    def addTryCatch(self, code_snippet, ratio=0.5):

        tree = self.parse(code_snippet)
        statements = self.get_statement_nodes(code_snippet, tree.root_node)

        oriContent = code_snippet.encode()
        content = code_snippet.encode()
        total = len(statements) - 1
        sample_num = math.ceil((total + 1) * ratio)
        ran = [random.randint(0, total) for i  in range(sample_num)]
        ran = set(ran)
        print(ran, total)
        origin_pos = []
        for idx in ran:
            child = statements[idx][0]
            origin_pos.append((idx, child.start_byte, child.end_byte))

        total = len(statements) - 1
        #  reverse
        for i, (start, end) in enumerate(origin_pos):
            tokenByte = self.getTokenByte(statements[i][0], oriContent)
            content = content[:start] + tokenByte + content[end:]
            # print(i, start, end, tokenByte.decode())
        return statements, content.decode()

    def getTokenByte(self, child, content):
        return content[child.start_byte:child.end_byte]

    def get_statement_nodes(self, code, root):
        queue = [root]
        statements = []
        content = code.encode()
        statement_types = ['expression_statement']
        ignore_types = ['labeled_statement']
        while queue:
            current_node = queue.pop(0)
            for child in current_node.children:
                child_type = str(child.type)
                if child_type in ignore_types:
                    continue
                token = self.getTokenByte(child, content).decode()
                if child_type in statement_types:
                    # if self.checkChild(child):
                    # captures = self.query.captures(child)
                    statements.append((child, token))
                else:
                    # don't append child
                    queue.append(child)

                # captures = None
                # print(child.sexp(), token )
                # print(child, token)
        return statements


def main():
    addTryCatch = AddTryCatch(language="java")

    sample_codes = [
        """
        public class Main {
          public static void main(String[] args) {
            int a = 15;
            Test.func1(a);
            circle.circumference(100, 20);
            if (b > 12) {
                label123: println("continuing");
                System.out.println("hello");
                continue;
                break;
                ;
                return 1;
            }
          }
        }
        """,
        """
        void bubbleSort(int arr[], int n)
        {
           int i, j;
           for (i = 0; i < n-1; i++)     
         
               // Last i elements are already in place  
               for (j = 0; j < n-i-1; j++)
                   if (arr[j] > arr[j+1])
                      swap(&arr[j], &arr[j+1]);
        }
        """
    ]

    for sample_code in sample_codes:
        statements, code = addTryCatch.addTryCatch(sample_code)
        print("-" * 50)
        for i in statements:
            print(i)
        print("-" * 50)
        print(code)
        break


if __name__ == "__main__":
    main()
