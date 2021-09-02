#include <stdio.h>
#include <string.h>

int main()
{
    unsigned long st1 = 0, st2 = 0;
    char c;
    long n = 1;
    long ks = 0;
    scanf("%c", &c);
                while(c != 32)
                {
                    if(c < 91) st1 = (st1 | (n << (c-65)));
                    else st1 = (st1 | (n << (c-71)));
                    scanf("%c", &c);
                }
                scanf("%c", &c);
                while(c != 10)
                {
                    if(c < 91) st2 = (st2 | (n << (c-65)));
                    else st2 = (st2 | (n << (c-71)));
                    scanf("%c", &c);
                }
                st1 = st1 & st2;
                for(int i = 0; i < 58; i++)
                {
                    if(((st2 >> i) & 1) * ((st1 >> i) & 1) == 1)
                    {
                        if(i < 26) printf ("%c", (i+65));
                        else printf ("%c", (i+71));
                    }
                }
                return 0;
            }
    