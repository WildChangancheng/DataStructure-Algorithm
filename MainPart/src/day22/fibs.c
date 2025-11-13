int get(int n, int* stack) {
        switch (n) {
            case 0: return 0;
            case 1: return 1;
            default:
                if (stack[n]!= 0) return stack[n];
                stack[n] = get(n-1, stack) + get(n-2, stack);
                return stack[n];
        }
}

// 自上而下的备忘录写法
int fib(int n) {
    if (n == 0 || n == 1) return n;
    int *stack = (int *) calloc(n+1, sizeof(int));
    stack[0] = 0;
    stack[1] = 1;
    return get(n, stack);
}

// 自下而上的dp table写法
int fib(int n) {
    if (n == 0 || n == 1) return n;
    int *stack = (int *) calloc(n+1, sizeof(int));
    stack[0] = 0;
    stack[1] = 1;
    for (int i = 2; i <= n; i++) stack[i] = stack[i-2] + stack[i-1];
    return stack[n];
}