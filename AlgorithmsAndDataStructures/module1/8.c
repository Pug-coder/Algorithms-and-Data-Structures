#include <stdio.h>
#include <stdlib.h>
 
int main()
{
    int n1, n2;
    scanf("%d", &n1);
    int *a= (int*)malloc(n1*sizeof(int));
 
    for (int i=0; i < n1; i++)
        scanf("%d", &a[i]);
 
    scanf("%d", &n2);
    int *b= (int*)malloc(n2*sizeof(int));
 
    for (int i=0; i < n2; i++)
        scanf("%d", &b[i]);
 
    int i = 0, j = 0;
    while(i < n1 && j < n2)
        printf("%d ", a[i] < b[j] ? a[i++] : b[j++]);
 
    for(int k = (i < n1 ? i : j); k < (i < n1 ? n1 : n2) ; k++)
        printf("%d ", (j < n2 ? b : a)[k]);
 
    free(a);
    free(b);
    return 0;
}