from pydantic import BaseModel
from agents import RunContextWrapper, Agent, ModelSettings, TResponseInputItem, Runner, RunConfig

class OkosotthonParancsElemzoSchema(BaseModel):
  room: str
  device: str
  command: str


class OkosotthonParancsElemzoContext:
  def __init__(self, workflow_input_as_text: str):
    self.workflow_input_as_text = workflow_input_as_text
def okosotthon_parancs_elemzo_instructions(run_context: RunContextWrapper[OkosotthonParancsElemzoContext], _agent: Agent[OkosotthonParancsElemzoContext]):
  workflow_input_as_text = run_context.context.workflow_input_as_text
  json_template = '{"room": "", "device": "", "command": ""}'
  return f"""Elemezd a felhasználó mondatát, és azonosítsd az okosotthon helyiségét, az érintett eszközt és a végrehajtandó parancsot.

Válaszolj kizárólag a következő JSON formátumban angolul:
{json_template}

Ha valami nem egyértelmű, a megfelelő mezőbe írd be, a legvalószínűbb választ.

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
    context=OkosotthonParancsElemzoContext(workflow_input_as_text=workflow["input_as_text"])
  )

  conversation_history.extend([item.to_input_item() for item in okosotthon_parancs_elemzo_result_temp.new_items])

  okosotthon_parancs_elemzo_result = {
    "output_text": okosotthon_parancs_elemzo_result_temp.final_output.json(),
    "output_parsed": okosotthon_parancs_elemzo_result_temp.final_output.model_dump()
  }
  
  return okosotthon_parancs_elemzo_result