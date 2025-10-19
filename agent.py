from pydantic import BaseModel
from agents import RunContextWrapper, Agent, ModelSettings, TResponseInputItem, Runner, RunConfig
import json


class OkosotthonParancsElemzoSchema(BaseModel):
  location: str
  device: str
  command: str
  missing_information: str
  result: str
  tokens_used: int


class OkosotthonParancsElemzoContext:
  def __init__(self, workflow_input_as_text: str, available_values: dict):
    self.workflow_input_as_text = workflow_input_as_text
    self.available_values = available_values

def okosotthon_parancs_elemzo_instructions(run_context: RunContextWrapper[OkosotthonParancsElemzoContext], _agent: Agent[OkosotthonParancsElemzoContext]):
  workflow_input_as_text = run_context.context.workflow_input_as_text
  
  # Extract available values
  available_values = run_context.context.available_values
  locations = available_values.get("locations", [])
  devices = available_values.get("devices", [])
  commands = available_values.get("commands", [])
  
  return f"""Egy okosotthon asszisztens vagy. Elemezd a felhasználó mondatát, és azonosítsd az okosotthon helyiségét, az érintett eszközt és a végrehajtandó parancsot.

A házban csak az alábbi helyiségek, eszközök és parancsok léteznek:

📍 Elérhető helyiségek (locations):
{', '.join(locations)}

🔧 Elérhető eszközök (devices):
{', '.join(devices)}

⚡ Elérhető parancsok (commands):
{', '.join(commands)}

Mindig csak olyan helyiséget, eszközt és parancsot választhatsz, amelyek a fenti listában egyértelműen tudsz azonosítani.

Válaszolj angolul:
Ha valami nem egyértelmű, a \"missing_information\" mezőben kérj pontosítást magyarul, és a mezőt hagyd üresen.
Ha emelet van megadva de nincs megadva, hogy hányadik emelet, akkor a \"missing_information\" mezőben kérj pontosítást magyarul, és a mezőt hagyd üresen.
Ha a parancs \"increase\" vagy \"decrease\" és nincs megadva a mértékegység, akkor a \"missing_information\" mezőben kérj pontosítást magyarul, és a mezőt hagyd üresen.
Ha minden egyértelmű, a \"result\" mezőben foglald össze a végeredményt magyarul, és töltsd ki a mezőket.
Ha durva, vagy sértő kifejezést hallasz, akkor írd be a \"missing_information\" mezőbe \"ide figyelj te pencinger gyerek, ezért ráduszítom a robotjaimat és kitépik a szívedet \""
A felhasznált tokenek számát a \"tokens_used\" mezőben add meg.

Most elemezd a következő mondatot:
{workflow_input_as_text}
"""
okosotthon_parancs_elemzo = Agent(
  name="okosotthon_parancs_elemzo",
  instructions=okosotthon_parancs_elemzo_instructions,
  model="gpt-4o-mini",
  output_type=OkosotthonParancsElemzoSchema,
  model_settings=ModelSettings(
    temperature=1,
    top_p=1,
    max_tokens=2048,
    store=True
  )
)


class WorkflowInput(BaseModel):
  input_as_text: str
  available_values: dict


# Main code entrypoint
async def run_workflow(workflow_input: WorkflowInput):
  state = {

  }
  workflow = workflow_input.model_dump()
  conversation_history: list[TResponseInputItem] = [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": workflow["input_as_text"]
        }
      ]
    }
  ]
  okosotthon_parancs_elemzo_result_temp = await Runner.run(
    okosotthon_parancs_elemzo,
    input=[
      *conversation_history
    ],
    run_config=RunConfig(trace_metadata={
      "__trace_source__": "agent-builder",
      "workflow_id": "wf_68e8905d38a48190a66d5d020d5ba56f0d25030eaf71b148"
    }),
    context=OkosotthonParancsElemzoContext(
      workflow_input_as_text=workflow["input_as_text"],
      available_values=workflow["available_values"]
    )
  )
  okosotthon_parancs_elemzo_result = {
    "output_text": okosotthon_parancs_elemzo_result_temp.final_output.json(),
    "output_parsed": okosotthon_parancs_elemzo_result_temp.final_output.model_dump()
  }
  
  return okosotthon_parancs_elemzo_result
