#include <stdio.h>
int main()
{
	int n, a1, a2, c = 2; //вводим по два числа;
	scanf("%i", &n);
	if(n == 1)
	{
		scanf("%i", &a1);
		if(a1 == 1) printf("0 1\n");
		else if(a1 == 0) printf("1\n");
	}
	else if(n == 2)
	{
		scanf("%i %i", &a1, &a2);
		printf("0 0 1\n");
	}
	else
	{
		scanf("%i %i", &a1, &a2);
		if(a1 == 0 && a2 == 1)
		{
			while(a1 == 0 && a2 == 1 && c < n)
			{
				printf("0 0 ");
				if(c < n)
				{
					c+= 2;
					scanf("%i %i", &a1, &a2);
				}
			}
			if(c < n)
			{
				printf("%i %i ", 1, a2);
				for(int i = c; i < n; i++)
				{
					scanf("%i", &a1);
					printf("%i ", a1);
				}
			}
			else printf("0 0 1");
		}
		else if (a1 == a2)
        {
            printf("%i %i ", 1, a2);
            for (int i = c; i < n; i++)
            {
                scanf("%i", &a1);
                printf("%i ", a1);
            }
        }
		else
		{
			printf("0 ");
			a1 = a2;
			scanf("%i", &a2);
			c = 3;
			while(a1 == 0 && a2 == 1 && c < n)
			{
				printf("0 0 ");
				if(c < n)
				{
					c+= 2;
					scanf("%i %i", &a1, &a2);
				}
			}
			if(a2 == 1) printf("0 0 1");
			else printf("%i %i ", 1, a2);
			for(int i = c; i < n; i++)
			{
				scanf("%i", &a1);
				printf("%i ", a1);
			}
		}
	}
	return 0;
}