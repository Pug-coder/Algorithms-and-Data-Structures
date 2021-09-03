#include <stdio.h> 
int main(void) { 
int c = 0,i, j, n, k; 
scanf("%d %d", &k, &n); 
char a[n + 1]; 
for (i = 0; i < n + 1; i++) a[i] = 1;
a[0] = 0;
a[1] = 0; 
for (i = 0; i < n / 2 && i * i <= n; i++)
{ 	
	if(a[i] != 0)
	{
	for (j = 0; j < n / i + 1; j++) 
			{ 
				c = i * j;
				if (c <= n) a[c] = a[i] + a[j]; 
			}
	} 
}
for (i = 0; i < n + 1; i++)
{ 
	if (a[i] == k) printf("%d ", i); 
} 
return 0; 
}