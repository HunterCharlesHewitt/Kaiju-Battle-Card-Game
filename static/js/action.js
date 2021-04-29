choose_action = function (event) {
  console.log("action button");
  socket.action_selected = $(this).attr("id");
  $(".actionButton").css("background-color", "unset");
  $(this).css("background-color", "SeaGreen");
  if (socket.action_selected && socket.target_creature_selected) {
    $("#playCards").show();
  }
  return false;
};

choose_target = function (event) {
  console.log($(this).attr("id"));
  console.log("creature select");
  socket.target_creature_selected = $(this)
    .attr("id")
    .replace("SelectButton", "");
  $("#userButton .creatureSelectButton").css("background-color", "");
  $(this).css("background-color", "SeaGreen");
  if (socket.action_selected && socket.target_creature_selected) {
    $("#playCards").show();
  }
  return false;
};

play_cards = function (event) {
  socket.emit("local_action_event", {
    user_id: socket.id,
    user_creature: socket.id_to_character[socket.id],
    target_user_id: socket.character_to_id[socket.target_creature_selected],
    target_creature: socket.target_creature_selected,
    action: socket.action_selected,
  });

  $("#playCards").hide();
  $("#waiting").show();
  $("#userButton .creatureSelectButton").css("background-color", "");
  $("#userButton .creatureSelectButton").attr("disabled", "disabled");
  $(".actionButton").attr("disabled", "disabled");
  $(".actionButton").css("background-color", "unset");
  return false;
};
