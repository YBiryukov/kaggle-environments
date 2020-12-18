async function renderer(context) {
  const {
    environment,
    parent,
    step
  } = context;

  const state = environment.steps[step + 1];
  const canvasWidth = environment.configuration.canvasSize[0];
  const canvasHeight = environment.configuration.canvasSize[1];

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
    // draw recharge station
    ctx.fillStyle = "#0567a8";
    const rechargeStation = state[0].observation.rechargeStation
    ctx.fillRect(rechargeStation.x, rechargeStation.y, rechargeStation.size.x, rechargeStation.size.y);

    // draw seed storage
    ctx.fillStyle = "#decf31";
    const seedStorage = state[0].observation.seedStorage
    ctx.fillRect(seedStorage.x, seedStorage.y, seedStorage.size.x, seedStorage.size.y);

    // draw planting sites
    state[0].observation.targets.forEach(function (target) {
      if (target.seeds_to_plant > 0) {
        ctx.fillStyle = "Green";
      } else {
        ctx.fillStyle = "#8f6c29";
      };
      ctx.beginPath();
      ctx.arc(target.x, target.y, target.size, 0, Math.PI*2, true);
      ctx.fill();
    });

    // draw drones
    ctx.fillStyle = "White";
    state[0].observation.drones.forEach(function (drone) {
      ctx.beginPath();
      ctx.arc(drone.position.x, drone.position.y, drone.size.width, 0, Math.PI*2, true);
      ctx.fill();
    });

    // draw ID's of drones
    ctx.fillStyle = "Black";
    state[0].observation.drones.forEach(function (drone) {
      ctx.fillText(drone.index, drone.position.x - drone.size.width, drone.position.y + drone.size.width * 0.5);
    });
  };
};
