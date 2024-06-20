from huggingface_hub import HfApi, file_exists
import os

def another():

    hf_token = os.getenv("HF_TOKEN")
    print(hf_token)
    api = HfApi(token=hf_token)
    model_info = api.model_info(
            repo_id="dknoller/test-model-upload", revision="0d4736eeaf7c582daf869c8070e4f890e54fa4db", timeout=10, files_metadata=True
        )
    size = sum(repo_file.size for repo_file in model_info.siblings)
    # print(size)
    x = model_info.lastModified.isoformat()
    print(x)

    api.hf_hub_download(
            repo_id="dknoller/test-model-upload",
            revision="387ad6a81e87b6445f961f597ada19d3f636fe00",
            filename="checkpoint.safetensors",
            cache_dir="./var",
        )

def evaluate_test(miner_scores):
    import torch
    import random

    # Generate synthetic scores for models
    synthetic_scores = []
    sample_min = 8

    # First set of models with baseline performance
    for i in range(10):
        synthetic_scores.append(random.random() * 0.01 + 0.86)

    # Second set of models with better performance
    for i in range(10):
        synthetic_scores.append(random.random() * 0.01 + 0.876)

    synthetic_scores = torch.tensor(synthetic_scores)

    # Function to compute win count
    def compute_win_simple(scores):
        wins = []
        for i in range(len(scores)):
            win = 0
            for j in range(len(scores)):
                if i > j:
                    if scores[i] * 0.97 > scores[j]:
                        win += 1
                elif i < j:
                    if scores[i] > scores[j] * 0.97:
                        win += 1
            wins.append(win)
        return wins

    # Compute win counts for the initial set of models
    wins = compute_win_simple(synthetic_scores)
    print(f'First round win count: {wins}')

    # Sample-based evaluation
    sampled_scores = synthetic_scores[torch.argsort(torch.tensor(wins), descending=True)[:sample_min].sort().values]
    new_scores = []

    # Adding new models and re-evaluating
    for miner_score in miner_scores:
        new_score = miner_score
        sampled_scores = torch.cat([sampled_scores, torch.tensor([new_score])])
        wins = compute_win_simple(sampled_scores)
        sampled_scores = sampled_scores[torch.argsort(torch.tensor(wins), descending=True)[:sample_min].sort().values]
        new_scores.append(new_score)

    print(f'Sample-based top scores: {sampled_scores}')

    # Non-sample-based evaluation
    non_sampled_scores = torch.cat([synthetic_scores, torch.tensor(new_scores)])
    wins = compute_win_simple(non_sampled_scores)
    non_sampled_scores = non_sampled_scores[
        torch.argsort(torch.tensor(wins), descending=True)[:sample_min].sort().values]

    print(f'Non-sample-based top scores: {non_sampled_scores}')