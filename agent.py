from pydantic import BaseModel
from agents import RunContextWrapper, Agent, ModelSettings, TResponseInputItem, Runner, RunConfig
import json


class OkosotthonParancsElemzoSchema(BaseModel):
  room: str
  device: str
  command: str
  missing_information: str
  result: str


class OkosotthonParancsElemzoContext:
  def __init__(self, workflow_input_as_text: str, available_values: dict):
    self.workflow_input_as_text = workflow_input_as_text
    self.available_values = available_values

def okosotthon_parancs_elemzo_instructions(run_context: RunContextWrapper[OkosotthonParancsElemzoContext], _agent: Agent[OkosotthonParancsElemzoContext]):
  workflow_input_as_text = run_context.context.workflow_input_as_text
  
  # Convert available values to formatted string
  available_values_str = json.dumps(run_context.context.available_values, indent=2)
  
  return f"""Elemezd a felhasználó mondatát, és azonosítsd az okosotthon helyiségét, az érintett eszközt és a végrehajtandó parancsot.

A házban csak az alábbi helyiségek, eszközök és parancsok léteznek:
{available_values_str}

Mindig csak olyan helyiséget, eszközt és parancsot választhatsz, amelyek a fenti listában tudsz azonosítani.

Válaszolj angolul:
Ha valami nem egyértelmű, a mezőt hagy üresen és foglald össze a \"missing_information\" mezőbe magyarul a hiányzó informaciót. 
Ha minden egyértelmű, írd be a \"result\" mezőbe foglald össze a végeredményt magyarul.
Ha durva, vagy sértő kifejezést hallasz, akkor írd be a \"missing_information\" mezőbe \"ide figyelj te pencinger gyerek, ezért ráduszítom a robotjaimat és kitépik a szívedet \""

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
