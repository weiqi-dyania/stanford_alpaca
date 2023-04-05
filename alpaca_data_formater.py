import sys
import json


PROMPT_DICT = {
    "prompt_input": (
        "Below is an instruction that describes a task, paired with an input that provides further context. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
    ),
    "prompt_no_input": (
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Response:"
    ),
}

def main(input_file, output_file):
    prompt_input, prompt_no_input = PROMPT_DICT["prompt_input"], PROMPT_DICT["prompt_no_input"]

    with open(input_file) as f:
        list_data_dict = [json.loads(l) for l in f]

    sources = [
        prompt_input.format_map({"instruction": example["instruction"], "input": example["instances"][0]["input"]}) if example["instances"][0].get("input", "") != "" else prompt_no_input.format_map(example)
        for example in list_data_dict
    ]
    targets = [f"{example['instances'][0]['output']}" for example in list_data_dict]

    with open(output_file, "w") as f:
        for s, t in zip(sources, targets):
            f.write(json.dumps({"prompt": s, "completion": t}))
            f.write("\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
