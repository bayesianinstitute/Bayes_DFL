import sys
from mqtt_operations import MqttOperations
from ml_operations import MLOperations
from utils import Utils
import argparse

from core.FL_System.identifyparticipants.identify_participants import IdentifyParticipant
import time
import uuid

# Define a class for the Federated Learning Workflow
class DFLWorkflow:
    def __init__(self,
                 broker_service,
                 global_cluster_topic,
                 internal_cluster_topic,
                 id,
                 voting_topic,
                 declare_winner_topic,
                 min_node,
                 updated_broker,
                 training_type,
                 optimizer,
                 ):
        # Initialize various attributes and parameters
        self.global_ipfs_link = None
        self.participant_identification = None
        self.broker_service = broker_service
        self.internal_cluster_topic = internal_cluster_topic
        self.global_cluster_topic = global_cluster_topic
        self.mqtt_operations = None
        self.ml_operations = MLOperations(training_type, optimizer)
        self.utils = Utils()
        self.global_model = None

        self.voting_topic = voting_topic
        self.winner_declare = declare_winner_topic

        self.id = f'{id}-{uuid.uuid4()}'  # Create a unique client ID with a UUID
        self.is_status = None
        self.min_node = min_node
        self.updated_broker = updated_broker

    # Function to terminate the program
    def terminate_program(self):
        print("Terminated program successfully ")
        sys.exit()

    # Main function to run the federated learning workflow
    def run(self):
        try:
            get_list = None
            # Create an instance of IdentifyParticipant and  to do voting if the client is a worker or head
            self.participant = IdentifyParticipant(
                self.id, self.broker_service, self.voting_topic, self.winner_declare, self.min_node)
            self.is_status = self.participant.main()
            print("Is worker head:", self.is_status)

            # Initialize  MQTT operations for communication
            self.mqtt_operations = MqttOperations(self.internal_cluster_topic,
                                                self.global_cluster_topic,
                                                self.broker_service,
                                                self.min_node,
                                                self.is_status,
                                                self.id)

            # Start, initialize, and get MQTT communication object
            mqtt_obj = self.mqtt_operations.start_dfl_using_mqtt()

            # Subscribe to all internal messages
            mqtt_obj.subscribe_to_internal_messages()

            Round_Counter = 0

            head_id=mqtt_obj.get_head_node_id()
            print("head_id : {}".format(head_id))
            # self.terminate_program()


            while True:
                # Check the termination status, and if True, close the program
                if mqtt_obj.terimate_status:
                    self.terminate_program()

                Round_Counter = Round_Counter + 1
                print("Round_Counter:", Round_Counter)



                if head_id:
                    mqtt_obj.send_head_id(head_id)
                    time.sleep(9)


                mqtt_obj.receive_internal_messages()


                while not mqtt_obj.head_id :
                    print("Waiting for to set head_id: ")
                    time.sleep(3)
                    pass
                print("Head_Id: ", mqtt_obj.head_id)
                
                self.terminate_program()

                ## Temporary to check if changing broker works or not program
                # if Round_Counter == 2:
                #     print("Changing Broker")
                #     time.sleep(10)
                #     mqtt_obj.switch_broker(self.updated_broker)

                # Train the model and get the model hash from IPFS
                hash = self.ml_operations.train_machine_learning_model()
                print("Model hash:", hash)

                # Send the model to the internal cluster
                mqtt_obj.send_internal_messages_model(hash)

                mqtt_obj.receive_internal_messages()

                # If head status is True, send, aggregate, and send the global model to all workers
                if self.is_status == True:

                    # Temporarily add send terminate message to all workers to close the program
                    if Round_Counter == 2:
                        print("Terminating by user")
                        # Send termination message
                        mqtt_obj.send_terminate_message("Terminate")

                        # Sleep for a fixed time
                        time.sleep(11)

                        # Terminate the program
                        self.terminate_program()

                    # Get a list of hashes from all workers in MQTT
                    get_list = mqtt_obj.get_all_hash()
                    print("Send global model:", get_list)

                    # Send all the list of hashes to aggregate and get the global model hash
                    self.global_model = self.ml_operations.aggregate_models(get_list)
                    print("Got Global model hash:", self.global_model)

                    # Sending global model hash to all workers
                    print(self.ml_operations.send_global_model_to_others(mqtt_obj, self.global_model))

                    # Clearing all previous model hashes from all workers
                    mqtt_obj.client_hash_mapping.clear()
                    print("Clear all hash operations")

                    # Get the latest global model hash
                    latest_global_model_hash = mqtt_obj.global_model()
                    print("I am aggregator, here is the global model hash:", latest_global_model_hash)

                    # Set the latest global model hash and set weights in MLOperation
                    self.ml_operations.is_global_model_hash(latest_global_model_hash)

                else:
                    # Get the latest global model hash
                    latest_global_model_hash = mqtt_obj.global_model()
                    print("I am not aggregator, got global model hash:", latest_global_model_hash)

                    # Set the latest global model hash and set weights in MLOperation
                    self.ml_operations.is_global_model_hash(latest_global_model_hash)

                # Temporary to close the program
                if Round_Counter == 6:
                    break

            print(f"Training completed with round {Round_Counter} !! ")
            
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("broker_service", help="Name of broker service", type=str)
    parser.add_argument("cluster_name", help="Name of the cluster", type=str)
    parser.add_argument("internal_cluster_topic", help="Internal Cluster topic", type=str)
    parser.add_argument("id", help="client_id", type=str)
    parser.add_argument("min_node", help="minimum Node", type=int)

    updated_broker = 'broker.hivemq.com'

    model_type = 'CNN'

    optimizer = 'adam'

    args = parser.parse_args()

    voting_topic = f'Voting topic on Cluster {args.cluster_name}'
    declare_winner_topic = f'Winner Topic on Cluster {args.cluster_name}'

    workflow = DFLWorkflow(args.broker_service, args.cluster_name, args.internal_cluster_topic, args.id,
                           voting_topic, declare_winner_topic, args.min_node, updated_broker, model_type, optimizer)

    workflow.run()
