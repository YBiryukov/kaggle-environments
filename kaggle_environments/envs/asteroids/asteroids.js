async function renderer(context) {
  const {
    environment,
    parent,
    step
  } = context;

  const state = environment.steps[step + 1];
  const canvasWidth = environment.configuration.canvasSize[0];
  const canvasHeight = environment.configuration.canvasSize[1];
  const shipFrame = environment.configuration.shipFrame;

  // canvas setup
  let canvas = parent.querySelector("canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    parent.appendChild(canvas);
  };
  canvas.width = canvasWidth;
  canvas.height = canvasHeight;
  const ctx = canvas.getContext("2d");
  // clear entire canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (step < environment.steps.length - 1) {
    // draw asteroids
    state[0].observation.asteroids.forEach(function (asteroid) {
      ctx.fillStyle = asteroid.color;
      ctx.beginPath();
      ctx.arc(asteroid.x, asteroid.y, asteroid.size, 0, Math.PI*2, true);
      ctx.fill();
    });

    // draw ships
    state[0].observation.shipsOfPlayers.forEach(function (playerShip) {
      // draw weapons
      ctx.fillStyle = "#a8a8a8";
      ctx.fillRect(playerShip.currentPosition.x, playerShip.currentPosition.y, shipFrame.weaponSize.x, shipFrame.weaponSize.y);
      ctx.fillRect(playerShip.currentPosition.x + shipFrame.size.x - shipFrame.weaponSize.x, playerShip.currentPosition.y, shipFrame.weaponSize.x, shipFrame.weaponSize.y);
      // draw cargo platform
      ctx.fillStyle = playerShip.platformColor;
      ctx.fillRect(playerShip.currentPosition.x + shipFrame.weaponSize.x, playerShip.currentPosition.y + shipFrame.platformSize.y, shipFrame.platformSize.x, shipFrame.platformSize.y);
      // draw player number on left weapon
      ctx.font = "15px Comic Sans MS";
      ctx.textAlign = "center";
      ctx.fillStyle = "black";
      ctx.fillText(playerShip.playerNumber, playerShip.currentPosition.x + shipFrame.weaponXCenter, playerShip.currentPosition.y + shipFrame.weaponYCenter);
      // draw cargo on the platform
      ctx.fillStyle = playerShip.platformColor;
      for(let i = 0; i < playerShip.platformCargoFilledSpace; i++) {
        ctx.fillRect(playerShip.currentPosition.x + shipFrame.weaponSize.x + shipFrame.platformCargoUnitSize.x * i, playerShip.currentPosition.y, shipFrame.platformCargoUnitSize.x, shipFrame.platformCargoUnitSize.y);
      };
      // draw projectiles
      ctx.fillStyle = "#60d60c";
      playerShip.projectiles.forEach(function (projectile) {
        ctx.fillRect(projectile[0], projectile[1], shipFrame.projectileSize.x, shipFrame.projectileSize.y);
      });
    });

    // draw scores of players on cargo platforms of ships
    state[0].observation.shipsOfPlayers.forEach(function (playerShip) {
      ctx.fillStyle = "white";
      ctx.fillText(playerShip.score, playerShip.currentPosition.x + shipFrame.shipXCenter, playerShip.currentPosition.y + shipFrame.size.y - 10);
    });
  };
};
