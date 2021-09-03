int strdiff(char *a, char *b)
{
	int i = 0;
	while(a[i] == b[i] && a[i] != '\0' && b[i] != '\0')
	{
		i++;
	}
	if(a[i] == '\0' && b[i] == '\0') return -1;
	int j = 0;
	char xor = a[i]^b[i]; 
	while(xor)
	{
		if(xor & 1) return 8 * i + j;
		xor = xor >> 1;
		j++;
	}
}