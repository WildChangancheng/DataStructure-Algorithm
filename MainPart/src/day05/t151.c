#include <stdio.h>
#include <string.h>
#include <ctype.h>

void reverse(char *s, int l, int r) {
    while (l < r) {
        char tmp = s[l];
        s[l] = s[r];
        s[r] = tmp;
        l++; r--;
    }
}

char* reverseWords(char* s) {
    int n = strlen(s);
    int i = 0, j = 0;

    while (i < n) {
        while (i < n && s[i] == ' ') i++;
        if (i >= n) break;
        if (j > 0) s[j++] = ' ';
        int start = j;
        while (i < n && s[i] != ' ') s[j++] = s[i++];
        reverse(s, start, j - 1);
    }
    s[j] = '\0';

    reverse(s, 0, j - 1);
    return s;
}
