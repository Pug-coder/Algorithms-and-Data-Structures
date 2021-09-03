#include <stdio.h>
int main()
{   
    long summax = 0, sumt = 0;
    int i, n, k, ch, indmax;
    scanf("%i %i", &n, &k);
    int a[k];
    for(i = 0; i < n; i++) 
    {   
        if(i < k)
        {
            scanf("%i", &a[i]);
            sumt+=a[i]; 
        }
        else
        {   
            int c = i % k;
            scanf("%i", &ch);
            sumt= sumt - a[c] + ch; 
            if(summax < sumt)
            { 
                indmax = i - k + 1;
                summax=sumt;
            }
            a[c] = ch;
        }
    }
    printf("%i", indmax);
    return 0;
}