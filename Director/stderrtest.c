#include <stdio.h>
#include <stdlib.h>
void main(int argc, char **argv) {
    int i;
    for (i = 1; i < argc; i++) {
        fprintf(stderr, "%s ", argv[i]);
    }
    fprintf(stderr, "\n");
    exit(0);
}
