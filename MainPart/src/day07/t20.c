bool isValid(char* s) {
    char *stack = calloc(1000000, sizeof(char));
    int i = 0;
    int pointer = 0;
    while (s[i] != '\0') {
        switch (s[i]) {
            case '(':
                stack[pointer] = 1;
                pointer ++;
                break;
            case '{':
                stack[pointer] = 2;
                pointer ++;
                break;
            case '[':
                stack[pointer] = 3;
                pointer ++;
                break;
            case ')':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 1) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
            case '}':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 2) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
            case ']':
                pointer --;
                if (pointer<0) return false;
                if (stack[pointer] == 3) {
                    stack[pointer] = 0;
                    break;
                }
                else return false;
        }
        i++;
    }
    if (pointer == 0) return true;
    return false;
}