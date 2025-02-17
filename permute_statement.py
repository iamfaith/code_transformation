from base_operator import BaseOperator
import random

# https://github.com/tree-sitter/py-tree-sitter


class PermuteStatement(BaseOperator):
    def __init__(self, language: str):
        super(PermuteStatement, self).__init__(language)
        # (method_invocation object: (identifier) name: (identifier) arguments: (argument_list))
        # (expression_statement (method_invocation object: (identifier) name: (identifier) arguments: (argument_list (decimal_integer_literal) (decimal_integer_literal))))
        method_q = '''
(method_invocation
  name: (identifier) @method)'''
        # https://github.com/nvim-treesitter/nvim-treesitter/blob/e01c7ce9727b9d18b71b41cc792cb4719e469598/queries/java/highlights.scm
        self.query = self.lang.query(method_q)

    def permute(self, code_snippet):

        tree = self.parse(code_snippet)
        statements = self.get_statement_nodes(code_snippet, tree.root_node)
        origin_pos = []
        for child, token in statements:
            origin_pos.append((child.start_byte, child.end_byte))
        random.shuffle(statements)
        oriContent = code_snippet.encode()
        content = code_snippet.encode()
        total = len(statements) - 1
        for i, (start, end) in enumerate(reversed(origin_pos)):
            tokenByte = self.getTokenByte(statements[total - i][0], oriContent)
            content = content[:start] + tokenByte + content[end:]
            print(i, start, end, tokenByte.decode())
            # print(content.decode())
        return statements, content.decode()

    def getTokenByte(self, child, content):
        return content[child.start_byte:child.end_byte]

    def checkChild(self, child):
        ignore_types = ['labeled_statement', 'method_invocation']
        queue = [child]
        while queue:
            current_node = queue.pop(0)
            for child in current_node.children:
                child_type = str(child.type)
                if child_type in ignore_types:
                    return False
        return True

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
    permuteStatement = PermuteStatement(language="java")

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
        permute_codes, code = permuteStatement.permute(sample_code)
        print("-" * 50)
        for i in permute_codes:
            print(i)
        print("-" * 50)
        print(code)
        break


if __name__ == "__main__":
    main()

# ('expression_statement', 'a = 100 * b;')
# ('labeled_statement', 'label123: println("continuing");')
# ('expression_statement', 'System.out.println("hello");')
# ('continue_statement', 'continue;')
# ('break_statement', 'break;')
# (';', ';')
