#!/bin/bash

set -e
TRAIN_OUTPUT_FOLDER=tasks_files_full_train
TEST_OUTPUT_FOLDER=tasks_files_full_test
# all tasks. 
TaskArray=('belief_state_generation toxic_classification document_grounded_generation nli_classification recovery_generation persuasion_strategy intent_classification schema_based_generation intent_present response_generation persuasion_generation persuasion_present beginswith_controlled_generation knowledge_grounded_generation act_classification question_generation eval_rating emotion_generation slot_value_generation gensf_slot_tagging relation_present slot_present find_incoherent_utterance summarization act_generation advice_generation endswith_controlled_generation emotion_tagging edit_generation db_based_generation find_swapped_utterance nontoxic_feedback_generation slot_tagging deal_present advice_present eval_ranking find_missing_utterance count_response_words persona_grounded_generation answer_selection eval_binary graph_based_generation dialfact_classification target_controlled_generation answer_generation response_generation_with_n_words keyword_controlled_generation relation_classification fill_missing_utterance')
#TaskArray=('edit_generation db_based_generation find_swapped_utterance nontoxic_feedback_generation slot_tagging deal_present advice_present eval_ranking find_missing_utterance count_response_words persona_grounded_generation answer_selection eval_binary graph_based_generation dialfact_classification target_controlled_generation answer_generation response_generation_with_n_words keyword_controlled_generation relation_classification fill_missing_utterance')
for val1 in ${TaskArray[*]}; do
	 echo "******"
     echo $val1
	 # 1000 training examples per task.
	 # 100 examples per test task.
	 echo "***"
	 echo "train"
	 python run_tasks.py --configfile configs/config_tasks2.json --task $val1 --max_data 10000 --tasks_output_folder tasks_files/$TRAIN_OUTPUT_FOLDER
	 echo "***"
	 echo "test"
	 python run_tasks.py --configfile configs/config_tasks2_test.json --task $val1 --max_data 1000 --tasks_output_folder tasks_files/$TEST_OUTPUT_FOLDER
	 echo $'\n'
done
