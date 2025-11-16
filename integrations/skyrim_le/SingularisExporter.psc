Scriptname SingularisExporter extends Quest
{
Exports Skyrim LE game state to JSON for Singularis AGI.

Installation:
1. Compile with Creation Kit
2. Attach to a quest that starts on game load
3. Ensure SKSE 1.7.3 is installed
4. Output: Data/SKSE/Plugins/singularis_state.json
}

; Update interval (seconds)
float Property UpdateInterval = 0.5 Auto

; Max NPCs to export
int Property MaxNPCs = 10 Auto

; Export file path
string Property ExportPath = "Data/SKSE/Plugins/singularis_state.json" Auto

Event OnInit()
    RegisterForSingleUpdate(UpdateInterval)
EndEvent

Event OnUpdate()
    ExportGameState()
    RegisterForSingleUpdate(UpdateInterval)
EndEvent

Function ExportGameState()
    Actor player = Game.GetPlayer()
    
    if !player
        return
    endif
    
    ; Build JSON manually (Papyrus doesn't have native JSON)
    string json = "{"
    
    ; Timestamp
    json += "\"timestamp\":" + Utility.GetCurrentRealTime() + ","
    
    ; Player data
    json += "\"player\":{"
    json += "\"id\":\"player\","
    
    ; Position
    float px = player.GetPositionX()
    float py = player.GetPositionY()
    float pz = player.GetPositionZ()
    json += "\"pos\":[" + px + "," + py + "," + pz + "],"
    
    ; Rotation
    float yaw = player.GetAngleZ()
    json += "\"facing_yaw\":" + yaw + ","
    
    ; Stats (normalized 0-1)
    float health = player.GetActorValue("Health")
    float healthMax = player.GetBaseActorValue("Health")
    float healthNorm = health / healthMax
    
    float stamina = player.GetActorValue("Stamina")
    float staminaMax = player.GetBaseActorValue("Stamina")
    float staminaNorm = stamina / staminaMax
    
    float magicka = player.GetActorValue("Magicka")
    float magickaMax = player.GetBaseActorValue("Magicka")
    float magickaNorm = magicka / magickaMax
    
    json += "\"health\":" + healthNorm + ","
    json += "\"stamina\":" + staminaNorm + ","
    json += "\"magicka\":" + magickaNorm + ","
    
    ; State
    bool sneaking = player.IsSneaking()
    bool inCombat = player.IsInCombat()
    bool weaponDrawn = player.IsWeaponDrawn()
    
    json += "\"sneaking\":" + sneaking + ","
    json += "\"in_combat\":" + inCombat + ","
    json += "\"weapon_drawn\":" + weaponDrawn
    
    json += "},"
    
    ; NPCs nearby
    json += "\"npcs\":["
    
    Actor[] nearbyActors = MiscUtil.ScanCellNPCs(player, 2000.0, MaxNPCs)
    int numActors = nearbyActors.Length
    
    int i = 0
    while i < numActors
        Actor npc = nearbyActors[i]
        
        if npc && npc != player && !npc.IsDead()
            if i > 0
                json += ","
            endif
            
            json += "{"
            
            ; ID
            string npcId = npc.GetBaseObject().GetName()
            if npcId == ""
                npcId = "npc_" + i
            endif
            json += "\"id\":\"" + npcId + "\","
            
            ; Position
            float nx = npc.GetPositionX()
            float ny = npc.GetPositionY()
            float nz = npc.GetPositionZ()
            json += "\"pos\":[" + nx + "," + ny + "," + nz + "],"
            
            ; Health
            float npcHealth = npc.GetActorValue("Health")
            float npcHealthMax = npc.GetBaseActorValue("Health")
            float npcHealthNorm = npcHealth / npcHealthMax
            json += "\"health\":" + npcHealthNorm + ","
            
            ; Relationship
            bool isEnemy = npc.IsHostileToActor(player)
            json += "\"is_enemy\":" + isEnemy + ","
            json += "\"is_alive\":true,"
            
            ; Distance
            float distance = player.GetDistance(npc)
            json += "\"distance_to_player\":" + distance + ","
            
            ; Line of sight (approximate)
            bool hasLOS = player.HasLOS(npc)
            json += "\"has_line_of_sight_to_player\":" + hasLOS + ","
            
            ; Awareness (0-1, based on detection)
            float awareness = 0.0
            if npc.IsDetectedBy(player)
                awareness = 0.5
            endif
            if npc.IsInCombat()
                awareness = 1.0
            endif
            json += "\"awareness_level\":" + awareness
            
            json += "}"
        endif
        
        i += 1
    endwhile
    
    json += "]"
    
    json += "}"
    
    ; Write to file
    MiscUtil.WriteToFile(ExportPath, json, false, false)
EndFunction
