extends CharacterBody3D

class_name Player

var speed = 300.0
var health = 100

func _ready():
	print("Player ready")

func take_damage(amount: int) -> void:
	health -= amount
	if health <= 0:
		die()

func die():
	queue_free()

func move_towards(target: Vector3):
	var direction = (target - global_position).normalized()
	velocity = direction * speed
	move_and_slide()
