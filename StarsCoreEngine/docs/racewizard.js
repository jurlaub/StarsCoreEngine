var prtCost = [40,95,45,10,-100,-150,120,180,90,-66];
var lrtCost = [-235,-25,-159,-201,40,-240,-155,160,240,255,325,180,70,30];
var scienceCost = [150,330,540,780,1050,1380];
var statsMin =[7,5,5,5,5,2,5,0,0,0,0,0,0,0,0,0];
var statsMax =[25,15,25,25,25,15,25,6,2,2,2,2,2,2,9,0];

var PRT_HE =0;
var PRT_SS =1;
var PRT_WM =2;
var PRT_CA =3;
var PRT_IS =4;
var PRT_SD =5;
var PRT_PP =6;
var PRT_IT =7;
var PRT_AR =8;
var PRT_JT =9;

var GRBIT_LRT_IFE	=0;
var GRBIT_LRT_TT	=1;
var GRBIT_LRT_ARM	=2;
var GRBIT_LRT_ISB	=3;
var GRBIT_LRT_GR	=4;
var GRBIT_LRT_UR	=5;
var GRBIT_LRT_MA	=6;
var GRBIT_LRT_NRSE	=7;
var GRBIT_LRT_CE	=8;
var GRBIT_LRT_OBRM	=9;
var GRBIT_LRT_NAS	=10;
var GRBIT_LRT_LSP	=11;
var GRBIT_LRT_BET	=12;
var GRBIT_LRT_RS	=13;

var GRBIT_TECH75_LVL3	=29;
var GRBIT_FACT_GER_LESS	=31;

var STAT_RES_PER_COL	=0;
var STAT_TEN_FAC_RES	=1;
var STAT_FAC_COST	=2;
var STAT_FAC_OPERATE	=3;
var STAT_TEN_MINES_PROD	=4;
var STAT_MINE_COST	=5;
var STAT_MINE_OPERATE	=6;
var STAT_SPEND_LEFTOVER	=7;
var STAT_ENERGY_COST	=8;	//0 if expensive, 1 if normal, 2 if cheap
var STAT_WEAP_COST	=9;
var STAT_PROP_COST	=10;
var STAT_CONST_COST	=11;
var STAT_ELEC_COST	=12;
var STAT_BIO_COST	=13;
var STAT_PRT	=14;

var MAXCLICKS = 100;

// checking for hardcoded humanoids race. calculateAdvantagePoints() must be: 25
var raceName = 'Humanoids';
var player_centerHab = [50,50,50];
var player_lowerHab  = [15,15,15];
var player_upperHab  = [85,85,85];
var player_growthRate= 15;
var player_stats = [10,10,10,10,10,5,10,0,1,1,1,1,1,1,9,0];	//what does #15 mean?
var player_grbit=0;	//no LRTs at all
var player_cheaterFlag =0;

function IMMUNE(a)
{
  return ((a)==-1);
}

function getbit(composite, bitno)
{
	return ((composite&(1<<bitno))!=0)?1:0;
}

function setbit(composite,position,value)
{
  if ((composite&(1<<position))==value)	//nothing to change
    return composite;
  //toggle
  return(composite ^ (1<<position));
}

function terrafAdjust(centerHab,tmpHab,TerraformingFactor)
{
  var terrafRelated=centerHab-tmpHab;
  if (Math.abs(terrafRelated)<=TerraformingFactor) terrafRelated=0;
  else
    if (terrafRelated<0) terrafRelated+=TerraformingFactor;
    else terrafRelated-=TerraformingFactor;
  return terrafRelated;
}

//by the Jeffs, from Constantin Bryzgalin <constb@tomsk.ru>
function habPoints()
{
	var isTotalTerraforming;	//bool
	var advantagePoints,planetDesir;	//double
	var gravityRelated,temperatureRelated,radiationRelated;	//not quite, but somehow
	var h,i,j,k;
	var tmpHab,TerraformingFactor;
	var terrafCombo = [0,0,0], testHabStart = [0,0,0], testHabWidth = [0,0,0], iterNum = [0,0,0];
	var testPlanetHab = [0,0,0];
var debugString=''; var testedTotal=0;
	advantagePoints = 0.0;
	isTotalTerraforming = getbit(player_grbit,GRBIT_LRT_TT);

	for (h=0;h<3;h++) {
	    if (h==0)
		TerraformingFactor=0;		//TerraformingFactor[h,isTotalTerraforming] = [[0,0],[5,8],[15,17]];
	    else
		if (h==1)
		    TerraformingFactor = isTotalTerraforming?8:5;
		else
		    TerraformingFactor = isTotalTerraforming?17:15;
		//set up progressively wider testHabStart and testHabWidth arrays
	    for (i=0; i<3; i++) {
			if (player_centerHab[i]>MAXCLICKS || player_lowerHab[i]>MAXCLICKS || player_upperHab[i]>MAXCLICKS || player_centerHab[i]<0 || player_lowerHab[i]<0 || player_upperHab[i]<0) {
				if (!IMMUNE(player_centerHab[i]) && !IMMUNE(player_lowerHab[i]) && !IMMUNE(player_upperHab[i])) {
					player_centerHab[i]=player_lowerHab[i]=player_upperHab[i]=-1;
					player_cheaterFlag |= 0x10;
				}
			}

			if (player_centerHab[i]<0) {
				testHabStart[i] = 50;
				testHabWidth[i] = 11;
				iterNum[i] = 1;
			} else {
				testHabStart[i] = player_lowerHab[i]-TerraformingFactor;
				if (testHabStart[i]<0) testHabStart[i]=0;
				tmpHab = player_upperHab[i]+TerraformingFactor;
				if (tmpHab>MAXCLICKS) tmpHab=MAXCLICKS;
				testHabWidth[i] = tmpHab-testHabStart[i];
				iterNum[i] = 11;
			}
	    }
		/* loc_92AAC */
	    gravityRelated = 0.0;
	    for (i=0;i<iterNum[0];i++) {
        	if (i==0 || iterNum[0]<=1)
	        	tmpHab = testHabStart[0];
        	else
        		tmpHab = Math.floor((testHabWidth[0]*i) / (iterNum[0]-1)) + testHabStart[0];

        	if (h!=0 && player_centerHab[0]>=0) {
			terrafCombo[0] = terrafAdjust(player_centerHab[0],tmpHab,TerraformingFactor);
			tmpHab = player_centerHab[0] - terrafCombo[0];
        	}
        	testPlanetHab[0] = tmpHab;	//(BYTE)
		temperatureRelated = 0.0;
		for (j=0;j<iterNum[1];j++) {
	        	if (j==0 || iterNum[1]<=1)
		        	tmpHab = testHabStart[1];
        		else
        			tmpHab = Math.floor((testHabWidth[1]*j) / (iterNum[1]-1)) + testHabStart[1];

			if (h!=0 && player_centerHab[1]>=0) {
				terrafCombo[1] = terrafAdjust(player_centerHab[1],tmpHab,TerraformingFactor);
				tmpHab = player_centerHab[1] - terrafCombo[1];
			}
			testPlanetHab[1] = tmpHab;
			radiationRelated = 0;
			for (k=0;k<iterNum[2];k++) {
	        	   if (k==0 || iterNum[2]<=1)
		        	tmpHab = testHabStart[2];
			   else
				tmpHab = Math.floor((testHabWidth[2]*k) / (iterNum[2]-1)) + testHabStart[2];

				if (h!=0 && player_centerHab[2]>=0) {
					terrafCombo[2] = terrafAdjust(player_centerHab[2],tmpHab,TerraformingFactor);
					tmpHab = player_centerHab[2] - terrafCombo[2];
				}
				testPlanetHab[2] = tmpHab;

				planetDesir = planetValueCalc(testPlanetHab[0],testPlanetHab[1],testPlanetHab[2]);
//debugString+='Testing ('+testPlanetHab[0]+','+testPlanetHab[1]+','+testPlanetHab[2]+'): '+planetDesir+'<br>';
//debugString+=' value=' + planetDesir + '<br>';
//testedTotal++;
				tmpHab = terrafCombo[0]+terrafCombo[1]+terrafCombo[2];	//was terrafRelated
//debugString+=' tmpHab=' + tmpHab +'; TerraformingFactor='+ TerraformingFactor + '<br>';
				if (tmpHab>TerraformingFactor) {
					planetDesir -= tmpHab-TerraformingFactor;
					if (planetDesir<0) planetDesir=0;
				}
//debugString+='tmp planetDesir=' + planetDesir + '<br>';
				planetDesir *= planetDesir;
				switch (h) {
					case 0: planetDesir*=7; break;
					case 1: planetDesir*=5; break;
					default: planetDesir*=6;
				}
				radiationRelated+=planetDesir;
debugString+='tmp radiationRelated=' + radiationRelated + '<br>';
			}
			/* loc_92D34 */
			if (player_centerHab[2]>=0)
				radiationRelated = Math.floor((radiationRelated*testHabWidth[2])/100);
			else
				radiationRelated *= 11;

			temperatureRelated += radiationRelated;
debugString+='tmp temperatureRelated=' + temperatureRelated + '<br>';
		}
		if (player_centerHab[1]>=0)
			temperatureRelated = Math.floor((temperatureRelated*testHabWidth[1])/100);
		else
			temperatureRelated *= 11;

		gravityRelated += temperatureRelated;
debugString+='tmp gravityRelated=' + gravityRelated + '<br>';
	    }
	    if (player_centerHab[0]>=0)
		    gravityRelated = Math.floor((gravityRelated*testHabWidth[0])/100);
	    else
		    gravityRelated *= 11;
	    advantagePoints += gravityRelated;
debugString+='tmp advantagePoints=' + advantagePoints + '<br>';
	}
document.getElementById('showdata').innerHTML = testedTotal+'<br>'+debugString;
	return Math.round(advantagePoints/10.0);
}

//by the Jeffs, from Constantin Bryzgalin <constb@tomsk.ru>
function BoundsCheck()
{
	var i,tmp;

	for (i=0;i<3;i++) {
		if (IMMUNE(player_lowerHab[i])) {
			if (!IMMUNE(player_upperHab[i]) || !IMMUNE(player_centerHab[i])) {
				player_upperHab[i] = player_centerHab[i] = -1;
				player_cheaterFlag |= 0x10;
			}
		} else {
			if (player_lowerHab[i]<0) {
				player_lowerHab[i]=0;
				player_cheaterFlag |= 0x10;
			}
			if (player_lowerHab[i]>MAXCLICKS) {
				player_lowerHab[i]=MAXCLICKS;
				player_cheaterFlag |= 0x10;
			}
			if (player_upperHab[i]>MAXCLICKS) {
				player_upperHab[i]=MAXCLICKS;
				player_cheaterFlag |= 0x10;
			}
			if (player_lowerHab[i]>player_upperHab[i]) {
				player_lowerHab[i] = player_upperHab[i];
				player_cheaterFlag |= 0x10;
			}
			tmp = player_centerHab[i];
			if (tmp != (player_lowerHab[i] + (player_upperHab[i] - player_lowerHab[i])/2)) {
				tmp = player_lowerHab[i] + (player_upperHab[i] - player_lowerHab[i])/2;
				player_cheaterFlag |= 0x10;
			}
		}
	}

	if (player_growthRate > 20) {
		player_growthRate = 20;
		player_cheaterFlag |= 0x10;
	}
	if (player_growthRate < 1) {
		player_growthRate = 1;
		player_cheaterFlag |= 0x10;
	}

	for (i=0; i<16; i++) {
		if (player_stats[i] < statsMin[i]) {
			player_stats[i] = statsMin[i];
			player_cheaterFlag |= 0x10;
		}
		if (player_stats[i] > statsMax[i]) {
			player_stats[i] = statsMax[i];
			player_cheaterFlag |= 0x10;
		}
	}
}

//by the Jeffs, from Constantin Bryzgalin <constb@tomsk.ru>
function calculateAdvantagePoints()
{
	var points = 1650,hab;
	var PRT,grRateFactor,grRate,facOperate,tenFacRes,operPoints,costPoints,prodPoints,tmpPoints;	//signed short
	var i,j,bad_lrts;	//signed short

	BoundsCheck();
	PRT = player_stats[STAT_PRT];
	hab = div(habPoints(),2000);
alert('Step1: '+hab);
	grRateFactor = player_growthRate;
	grRate = grRateFactor;
	if (grRateFactor <= 5) {
	  points += (6-grRateFactor)*4200;
	} else {
	  if (grRateFactor <= 13) {
		switch(grRateFactor) {
			case 6: points+=3600;
				break;
			case 7: points+=2250;
				break;
			case 8: points+=600;
				break;
			case 9: points+=225;
				break;
		}
		grRateFactor=grRateFactor*2-5;
	  } else {
	    if (grRateFactor < 20) {
	      grRateFactor=(grRateFactor-6)*3;
	    } else {
	      grRateFactor = 45;
	    }
	  }
	}

	points -= div(hab*grRateFactor,24);

	i=0;	//immunity counter
	for (j=0; j<3; j++)
	{
		if (player_centerHab[j]<0) {
			i++;
		}
		else {
			points += Math.abs(player_centerHab[j] - 50)*4;
		}
	}
	if (i>1) points -= 150;

	facOperate = player_stats[STAT_FAC_OPERATE];
	tenFacRes = player_stats[STAT_TEN_FAC_RES];

	if (facOperate>10 || tenFacRes>10)
	{
		facOperate -= 9; if (facOperate<1) facOperate=1;
		tenFacRes  -= 9; if (tenFacRes<1) tenFacRes=1;

		tenFacRes *= (2+(PRT==PRT_HE?1:0));

		/*additional penalty for two- and three-immune*/
		if (i>=2)
			points -= div(((tenFacRes*facOperate)*grRate),2);
		else
			points -= div(((tenFacRes*facOperate)*grRate),9);
	}

	j = player_stats[STAT_RES_PER_COL];	//for AR, too
	if (j>25) j=25;
	if (j<=7) points -= 2400;
	else if (j==8) points -=1260;
	else if (j==9) points -= 600;
	else if (j>10) points += (j-10)*120;

	if (PRT != PRT_AR) {
		/*factories*/
		prodPoints = 10-player_stats[STAT_TEN_FAC_RES];
		costPoints = 10-player_stats[STAT_FAC_COST];
		operPoints = 10-player_stats[STAT_FAC_OPERATE];
		tmpPoints=0;

		if (prodPoints>0) tmpPoints=prodPoints*100;
		else tmpPoints+=prodPoints*121;
		if (costPoints>0) tmpPoints+=costPoints*costPoints*(-60);
		else tmpPoints+=costPoints*(-55);
		if (operPoints>0) tmpPoints+=operPoints*40;
		else tmpPoints+=operPoints*35;

		if (tmpPoints>700) tmpPoints = div((tmpPoints-700),3)+700;

		if (operPoints<=-7) {
			if (operPoints<-11) {
				if (operPoints<-14) tmpPoints-=360;
				else tmpPoints+=(operPoints+7)*45;
			} else tmpPoints+=(operPoints+6)*30;
		}

		if (prodPoints<=-3) tmpPoints+=(prodPoints+2)*60;

		points += tmpPoints;

		if (getbit(player_grbit,GRBIT_FACT_GER_LESS) != 0) points-=175;

		/*mines*/
		prodPoints = 10-player_stats[STAT_TEN_MINES_PROD];
		costPoints = 3-player_stats[STAT_MINE_COST];
		operPoints = 10-player_stats[STAT_MINE_OPERATE];
		tmpPoints=0;

		if (prodPoints>0) tmpPoints=prodPoints*100;
		else tmpPoints+=prodPoints*169;
		if (costPoints>0) tmpPoints-=360;
		else tmpPoints+=costPoints*(-65)+80;
		if (operPoints>0) tmpPoints+=operPoints*40;
		else tmpPoints+=operPoints*35;

		points+=tmpPoints;
	}
	else points += 210; /* AR */

	/*LRTs*/
	points -= prtCost[PRT];
	i=bad_lrts=0;
	for(j=0;j<=13;j++) {
		if (getbit(player_grbit,j)!=0) {
			if (lrtCost[j]>=0) i++;
			else bad_lrts++;
			points+=lrtCost[j];
		}
	}
	if ((bad_lrts+i)>4) points -= (bad_lrts+i)*(bad_lrts+i-4)*10;
	if ((i-bad_lrts)>3) points -= (i-bad_lrts-3)*60;
	if ((bad_lrts-i)>3) points -= (bad_lrts-i-3)*40;

	if (getbit(player_grbit,GRBIT_LRT_NAS) != 0) {
		if (PRT == PRT_PP) points -= 280;
		else if (PRT == PRT_SS) points -= 200;
		else if (PRT == PRT_JT) points -= 40;
	}

	/*science*/
	tmpPoints=0;
	for (j=STAT_ENERGY_COST; j<=STAT_BIO_COST; j++)
	    tmpPoints += player_stats[j]-1;
	if (tmpPoints>0) {
		points -= tmpPoints*tmpPoints*130;
		if (tmpPoints==6) points+=1430;
		else if (tmpPoints==5) points+=520;
	} else if (tmpPoints<0) {
		points+=scienceCost[-tmpPoints-1];
		if (tmpPoints<-4 && player_stats[STAT_RES_PER_COL]<10) points-=190;
	}
	if (getbit(player_grbit,GRBIT_TECH75_LVL3) != 0) points-=180;
	if (PRT==PRT_AR && player_stats[STAT_ENERGY_COST]==2)	/*50% less*/
	  points -= 100;

	return div(points,3);	//Math.floor makes -3.6 -> -4!
}

function div(dividend,divisor)
{//subtract the modulus, then divide
   return ((dividend-(dividend%divisor))/divisor);
}

//exact reverse except when ambiguous input
function getClicksFromGrav(grav)
{
  grav *= 100;
  var result;
  var lowerHalf = 1;
  if (grav < 100) {
    grav = Math.floor(10000/grav);
    lowerHalf = -1;
  }
  if (grav < 200) {
    result = grav/4-25;
  } else {
    result = (grav + 400) / 24;
  }
  result = Math.floor(50.9+lowerHalf*result);
  if (result < 1) result = 1;	//one less ambiguity
  return result;
}

//by the Jeffs, from Constantin Bryzgalin <constb@tomsk.ru>
function gravityFromGravityPoints(grav)
{
    var dist2Center = Math.abs(grav-50);	// a symmetrical curve
    var result;
    if (dist2Center<=25) {
	result = (dist2Center+25)*4;
    } else {
	result = dist2Center*24-400;
    }

    if (grav<50) {	//lower half is inverted
	result = 10000/result;
    }

    return (Math.floor(result)/100);
}

function tempFromTempPoints(temp)
{
    return(temp-50)*4;
}

//by the Jeffs, from Constantin Bryzgalin <constb@tomsk.ru>
//in: an array of 3 bytes from 0 to 100
//out: a signed integer between -45 and 100
function planetValueCalc(Grav, Temp, Rad)
{
  var planetHabData = new Array(Grav, Temp, Rad);	//in clicks 0..100
  var planetValuePoints=0,redValue=0,ideality=10000;	//in fact, they are never < 0
  var planetHab,habUpper,habLower,habCenter;
  var Excentr,habRadius,margin,Negativ,dist2Center;

  for (var i=0; i<3; i++) {
    habUpper  = player_upperHab[i];
    if (IMMUNE(habUpper)) {	//perfect hab
      planetValuePoints += 10000;
    }
    else {
      habLower  = player_lowerHab[i];
      habCenter = (habUpper+habLower)/2;	//no need to precalc, assuming data is legit
      planetHab = planetHabData[i];

	dist2Center = Math.abs(planetHab-habCenter);
	//if (habCenter > planetHab) {
	habRadius = habCenter-habLower;	// >= dist2Center if green
	//} else { habRadius = habUpper-habCenter; }	//different numbers, same result
	//if (habRadius != (habUpper-habCenter)) alert('oops!');
//      if ((habLower <= planetHab) && (planetHab <= habUpper)) {	/* green planet */
/*
 note: this version makes the basic assumption that habitability is
 symmetrical around the center, that is, the ideal center is located
 in the middle of the lower and upper boundaries, and both halves
 have the same value. The original algorithm seems able to cope with
 weirder definitions, i.e: bottom is 20, top is 80, center is 65,
 and hab value stretches proportionally to the different length of
 both "halves"...
*/
      if (dist2Center<=habRadius) {
	Excentr = 100 - Math.floor(100*dist2Center/habRadius);	//kind of reverse excentricity
	planetValuePoints += Excentr*Excentr;
	margin = dist2Center*2 - habRadius;
	if (margin>0) {	// hab in the "external quarters". dist2Center > 0.5*habRadius
	  ideality *= 3/2 - dist2Center/habRadius;	//(habRadius*2 - margin)/(habRadius*2)
	/*
	  ideality *= habRadius*2 - margin;	//better suited for integer math
	  ideality /= habRadius*2;		//decrease ideality up to ~50%
	*/
	  ideality = Math.floor(ideality);	//if margin==0, ideality doesn't change
	}
      } else {	/* red planet */
	//if (habLower < planetHab) {	//thus, planetHab>habUpper
	//  Negativ=planetHab-habUpper; } else { Negativ=habLower-planetHab; }
	Negativ = dist2Center-habRadius;
	if (Negativ>15) Negativ=15;
	redValue += Negativ;
      }
    }
  }

  if (redValue!=0) return -redValue;
  planetValuePoints = Math.floor(Math.sqrt(planetValuePoints/3)+.9);	//rounding a la Jeff
  planetValuePoints = planetValuePoints * ideality/10000;

  return Math.floor(planetValuePoints);
}

//calc terraformed values to feed to planetValueCalc
function terrafValueCalc(origGrav, origTemp, origRad, Grav, Temp, Rad)
{
  var planetHabOrig = new Array(origGrav, origTemp, origRad);
  var planetHab_Now = new Array(Grav, Temp, Rad);	//what if report is not current?
  var terrafData = new Array(origGrav, origTemp, origRad);
  var planetHab,habCenter,habUpper,habLower;
  for (var i=0; i<3; i++) {
    habUpper  = player_upperHab[i];
    if ((habUpper<0) || (player_terraf[i]<1)) {	//Immunity or no terraforming tech
      continue;		//no need to update
    }
    habLower  = player_lowerHab[i];
    habCenter = (habUpper+habLower)/2;
    planetHab = planetHabOrig[i];
    //shift planet's values towards ideal Center
    if (planetHab < habCenter) {
    	//alert(planetHab+1*player_terraf[i]);	//damn string addition!!
      terrafData[i] = Math.min(planetHab+1*player_terraf[i],habCenter);
    } else {
      terrafData[i] = Math.max(planetHab-1*player_terraf[i],habCenter);
    }
    //if current planet value is more centered than the race's terraf allows, take it!
    //the planet has been terraformed by someone with better terraf...
    if (Math.abs(terrafData[i]-habCenter) > Math.abs(planetHab_Now[i]-habCenter)) {
//alert("Preterraformed! "+terrafData[i]+'->'+habCenter+'<-'+planetHab_Now[i]);
      terrafData[i] = planetHab_Now[i];
    }
  //alert("Terrafvals["+i+"]:"+terrafData.join(","));
  }
  return planetValueCalc(terrafData[0],terrafData[1],terrafData[2]);
}
