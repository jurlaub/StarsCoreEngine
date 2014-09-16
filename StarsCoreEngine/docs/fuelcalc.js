//from Stars! engine guts: W1 to W10 Fuel Efficiency
var enginTab = [[0,0,0,0,0,0,140,275,480,576],
		[0,25,100,100,100,180,500,800,900,1080],
		[0,0,0,0,35,120,175,235,360,420],
		[0,20,60,100,100,105,450,750,900,1080],
		[0,20,60,70,100,100,110,600,750,900],
		[0,15,50,60,70,100,100,115,700,840],
		[0,15,35,45,55,70,80,90,100,120],
		[0,10,30,40,50,60,70,80,90,100],
		[0,0,0,0,0,65,75,85,95,105],
		[0,5,15,20,25,30,35,40,45,50],
		[0,0,0,0,0,0,165,375,600,720],
		[0,0,0,0,0,85,105,210,380,456],
		[0,0,0,0,0,0,88,100,145,174],
		[0,0,0,0,0,0,0,65,90,108],
		[0,0,0,0,0,0,0,0,70,84],
		[0,0,0,0,0,0,0,0,0,60]];

//Tested against 950+ actual trips using Interspace-10, Fuel Mizer, Galaxy
// Scoop, Enigma Pulsar and Trans-Star 10 engines, with and w/out IFE,
// with fleets, single ships, speeds over optimum, etc.
function FuelUsage(EngineID, Speed, FleetMass, Dist)
{
  //Here's a little surprise. It's perhaps done elsewhere but it
  // affects actual fuel usage and fools Stars! fuel display just
  // where it is noticed the most. Unintended, sure. ;-)
  if (Dist > Speed * Speed) {	//hinted at by Laertes in rgcs years ago
     Dist = Speed * Speed;	//sort of "extreme range" bonus
  }
  //spent fuel is calculated with the "sanity-checked" distance
  return( FuelCost(EngineID, Speed, FleetMass, Dist));
  //Note: the math is good for multi-hop distances, but full accuracy
  // mandates exact coordinates of all intermediate waypoints, which
  // should be calculated elsewhere.
}

//Actually consumed fuel calculation, based on AH's Stars! 2.6jRC4 figures.
//Everything is rounded up, yielding a quite non-linear staircase curve.
function FuelCost(EngineID, Speed, FleetMass, Dist)
{
//1 mg of fuel will move 200 kt of weight 1 LY at a Fuel Usage Number of 100.
//Number of engines doesn't matter. Neither number of ships with the same engine.

  var Distan = Math.ceil(Dist);	//rounding to next integer gives best graph fit
  //window.status = 'Actual distance used is ' + Distan + 'ly';

  //IFE is applied to drive specifications, just as the helpfile hints.
  //Stars! probably does it outside here once per turn per engine to save time.
  var EnginEff = Math.ceil(IFE * enginTab[EngineID-1][Speed-1]);

  //20000 = 200*100
  //Safe bet is Stars! does all this with integer math tricks.
  //Subtracting 2000 in a loop would be a way to also get the rounding.
  //Or even bitshift for the 2 and adjust "decimal point" for the 1000
  var teorFuel = Math.floor(FleetMass * EnginEff * Distan / 2000) / 10;
  //using only one decimal introduces another artifact: .0999 gets rounded down to .0

  //The heavier ships will benefit the most from the accuracy
  var intFuel = Math.ceil(teorFuel);
	//That's all. Nothing really fancy, much less random. Subtle differences in
	// math lib workings might explain the rarer and smaller discrepancies observed
  return(intFuel);
	//Unrelated to this fuel math are some quirks inside the
	// "negative fuel" watchdog when the remainder of the
	// trip is < 1 ly. Aahh, the joys of rounding! ;o)
}

//Stars! fuel guesstimator. Extended from single to multi-hops.
//Accurate enough, but not as thoroughly tested as the usage math
function fuelDisplay(EngineID, Speed, FleetMass, Distance)
{
  var SpeedRange = Speed * Speed;
	//We're assuming constant speed for the whole trip
  var numHops = Math.floor( Math.floor(Distance)/SpeedRange );	//first, whole hops at full warp
  var Fuelestimate = FuelCost(EngineID, Speed, FleetMass, SpeedRange) * numHops;	//ideally
	//remainder of trip
  Fuelestimate += FuelCost(EngineID, Speed, FleetMass, Distance - SpeedRange * numHops);
	//Blunders at extreme ranges, worse with heavy fleets.
  return(Fuelestimate);
}

function getMaxFreeSpeed(EngineID)
{
  for (var trialSpeed=1; enginTab[EngineID-1][trialSpeed-1]==0; trialSpeed++) {
     if (trialSpeed>10) {	//better safe than sorry
	alert(trialSpeed);
	break;
     }
  }
  return(trialSpeed-1);
}
