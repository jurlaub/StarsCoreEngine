	// checking for hardcoded humanoids race
	player.centerHab[0]=player.centerHab[1]=player.centerHab[2]=50;
	player.lowerHab[0]=player.lowerHab[1]=player.lowerHab[2]=15;
	player.upperHab[0]=player.upperHab[1]=player.upperHab[2]=85;
	player.growthRate=15;
	player.stats[0]=10;
	player.stats[1]=10;
	player.stats[2]=10;
	player.stats[3]=10;
	player.stats[4]=10;
	player.stats[5]=5;
	player.stats[6]=10;
	player.stats[7]=0;
	player.stats[8]=1;
	player.stats[9]=1;
	player.stats[10]=1;
	player.stats[11]=1;
	player.stats[12]=1;
	player.stats[13]=1;
	player.stats[14]=9;
	player.stats[15]=0;
	player.grbit=0;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 25 << endl;

	// checking for hardcoded rabbitoids race
	player.centerHab[0]=33;	player.centerHab[1]=58;	player.centerHab[2]=33;
	player.lowerHab[0]=10;	player.lowerHab[1]=35;	player.lowerHab[2]=13;
	player.upperHab[0]=56;	player.upperHab[1]=81;	player.upperHab[2]=53;
	player.growthRate=20;
	player.stats[0]=10;
	player.stats[1]=10;
	player.stats[2]=9;
	player.stats[3]=17;
	player.stats[4]=10;
	player.stats[5]=9;
	player.stats[6]=10;
	player.stats[7]=4;
	player.stats[8]=0;
	player.stats[9]=0;
	player.stats[10]=2;
	player.stats[11]=1;
	player.stats[12]=1;
	player.stats[13]=2;
	player.stats[14]=7;
	player.stats[15]=0;
	player.grbit=0x80000503;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 32 << endl;

	// checking for hardcoded insectoids race
	player.centerHab[0]=-1;	player.centerHab[1]=50;	player.centerHab[2]=85;
	player.lowerHab[0]=-1;	player.lowerHab[1]=0;	player.lowerHab[2]=70;
	player.upperHab[0]=-1;	player.upperHab[1]=100;	player.upperHab[2]=100;
	player.growthRate=10;
	player.stats[0]=10;
	player.stats[1]=10;
	player.stats[2]=10;
	player.stats[3]=10;
	player.stats[4]=9;
	player.stats[5]=10;
	player.stats[6]=6;
	player.stats[7]=1;
	player.stats[8]=2;
	player.stats[9]=2;
	player.stats[10]=2;
	player.stats[11]=2;
	player.stats[12]=1;
	player.stats[13]=0;
	player.stats[14]=2;
	player.stats[15]=0;
	player.grbit=0x2108;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 43 << endl;

	// checking for hardcoded nucleotids race
	player.centerHab[0]=-1;	player.centerHab[1]=50;	player.centerHab[2]=50;
	player.lowerHab[0]=-1;	player.lowerHab[1]=12;	player.lowerHab[2]=0;
	player.upperHab[0]=-1;	player.upperHab[1]=88;	player.upperHab[2]=100;
	player.growthRate=10;
	player.stats[0]=9;
	player.stats[1]=10;
	player.stats[2]=10;
	player.stats[3]=10;
	player.stats[4]=10;
	player.stats[5]=15;
	player.stats[6]=5;
	player.stats[7]=0;
	player.stats[8]=0;
	player.stats[9]=0;
	player.stats[10]=0;
	player.stats[11]=0;
	player.stats[12]=0;
	player.stats[13]=0;
	player.stats[14]=1;
	player.stats[15]=0;
	player.grbit=0x2000000C;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 11 << endl;

	// checking for hardcoded silicanoids race
	player.centerHab[0]=-1;	player.centerHab[1]=-1;	player.centerHab[2]=-1;
	player.lowerHab[0]=-1;	player.lowerHab[1]=-1;	player.lowerHab[2]=-1;
	player.upperHab[0]=-1;	player.upperHab[1]=-1;	player.upperHab[2]=-1;
	player.growthRate=6;
	player.stats[0]=8;
	player.stats[1]=12;
	player.stats[2]=12;
	player.stats[3]=15;
	player.stats[4]=10;
	player.stats[5]=9;
	player.stats[6]=10;
	player.stats[7]=3;
	player.stats[8]=1;
	player.stats[9]=1;
	player.stats[10]=2;
	player.stats[11]=2;
	player.stats[12]=1;
	player.stats[13]=0;
	player.stats[14]=0;
	player.stats[15]=0;
	player.grbit=0x1221;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 9 << endl;

	// checking for hardcoded antetherals race
	player.centerHab[0]=15;	player.centerHab[1]=50;	player.centerHab[2]=85;
	player.lowerHab[0]=0;	player.lowerHab[1]=0;	player.lowerHab[2]=70;
	player.upperHab[0]=30;	player.upperHab[1]=100;	player.upperHab[2]=100;
	player.growthRate=7;
	player.stats[0]=7;
	player.stats[1]=11;
	player.stats[2]=10;
	player.stats[3]=18;
	player.stats[4]=10;
	player.stats[5]=10;
	player.stats[6]=10;
	player.stats[7]=0;
	player.stats[8]=2;
	player.stats[9]=0;
	player.stats[10]=2;
	player.stats[11]=2;
	player.stats[12]=2;
	player.stats[13]=2;
	player.stats[14]=5;
	player.stats[15]=0;
	player.grbit=0x5C4;

	cout << "adv points: " << calculateAdvantagePoints(&player) 
		<< "\t\tmust be: " << 7 << endl;
