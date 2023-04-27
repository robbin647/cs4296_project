import copy
from collections import defaultdict



def mySimulatorLoop(self, *, max_sim_duration=10 ** 10,
             delay_sched=False, delay=0, provision_gap=5,
             policies="req-cluster",
             evict_policy="dep-lru",
             evict_th=0.1,
             lb_ratio=None,
             hot_duration=0,
             ):
        '''
        self: exp.simulator.Simulator
            ref to a Simulator instance
        '''
        # save a deep copy of the node list
        node_list = copy.deepcopy(self.node_list)

        

        # store the results of interests such that the experiments can
        # conveniently obtain the them after a single run
        quick_results = defaultdict(list)

        for policy in policies:
            # reset metric and counters
            self.ty.reset()
            total_lat, total_provision_lat, accept_req_num, req_seq_pos = 0, 0, 0, 0
            evict_policy = evict_policy if policy == "dep" else "kube"
            retry_queue = []
            node_heatings = []

            # simulation loop
            for tick in range(max_sim_duration):
                # print(tick)
                # update cluster states, using t as the event signal
                sig = tick
                # print(self.node_heating_ratio())
                # if 0.5 * len(self.req_seq) < tick < len(self.req_seq):
                #     self.ty.tel_node_snap(self.node_list, image=True)


                if 0.0 * len(self.req_seq) < tick < len(self.req_seq):
                    node_heatings.append(self.node_heating_ratio())
                    # pdb.set_trace()
                    self.ty.tel_node_snap(self.node_list, image=False)

                self.update_nodes(sig, self.node_list, evict_policy=evict_policy, evict_th=self.evict_th)

                sig, req_node_pairs = tick, []
                # when the req_seq is exhausted, we end the simulation loop
                if tick >= len(self.req_seq):
                    req_batch = []
                    if len(retry_queue) == 0:
                        self.tr.set_metric("duration", tick)
                        break
                else:
                    # concatenate the retry_queue and the req_batch is equivalent of leaving
                    # unscheduled tasks in one single queue with new ones appended at the end
                    req_batch = [(sig, req) for req in self.req_list[req_seq_pos:req_seq_pos + self.req_seq[tick]]]
                    req_seq_pos += self.req_seq[tick]

                # print(len(retry_queue))
                req_batch = retry_queue + req_batch
                retry_queue = []

                # scheduling loop
                for submit_tick, req in req_batch:
                    pdb.set_trace()

                    # fast check if all nodes are full at the moment
                    if self.is_all_full(self.node_list):
                        retry_queue.append((submit_tick if submit_tick < sig else sig, req))
                        continue

                    # scheduler finds the node to place the request, -1 if failed
                    node_index = self.sched.schedule(req, self.node_list,
                                                     policy, lb_ratio=lb_ratio)
                    if node_index < 0:
                        self.ty.report_rej(node_index)
                        retry_queue.append((submit_tick if submit_tick < sig else sig, req))
                        continue

                    node = self.node_list[node_index]
                    provision_lat = self.calc_latency(req, node)
                    wait_time = (sig - submit_tick) * 1000 # time elapsed (in milliseconds) since this ``req`` was submitted

                    # delay scheduling
                    if delay_sched and policy == "dep":
                        # if the "best" node found still yields too high startup latency, wait a bit
                        if provision_lat > provision_gap * (1 + wait_time) and wait_time <= delay * 1000:
                            retry_queue.append((submit_tick if submit_tick < sig else sig, req)) # append a tuple: (min{submit_tick, sig}, req)
                            continue
                    # node placement
                    required_size = self.place_node(sig, req, node)
                    if node[2] + required_size > node[3] * (1 - evict_th):
                        free_size = self.evict_node(node,
                                                    evict_policy=evict_policy,
                                                    )
                    # collect metrics
                    lat = provision_lat + wait_time
                    total_lat += lat
                    total_provision_lat += provision_lat
                    accept_req_num += 1
                    self.tr.add_lat_result(lat)
                    self.tr.add_provision_lat_result(provision_lat)
                    self.ty.report_req(req)
                    # end of simulation loop

            # collect results
            if tick == max_sim_duration:
                print("--> max sim duration hit.")
                quick_results["util"].append(1)

            mean_startup_lat = -1.0
            if accept_req_num != 0:
                mean_startup_lat = round(total_lat / accept_req_num)

            mean_provision_lat = -1.0
            if accept_req_num != 0:
                mean_provision_lat = round(total_provision_lat / accept_req_num)

            self.tr.set_metric("mean_lat", mean_startup_lat) \
                .set_metric("mean_provision_lat", mean_provision_lat) \
                .set_metric("accept_req_num", accept_req_num) \
                .set_setup_metric("sched_policy", policy)

            quick_results["util"].append(self.ty.tel_util(total_provision_lat))
            quick_results["mean_provision_lat"].append(mean_provision_lat)
            quick_results["mean_startup_lat"].append(mean_startup_lat)

            # print and write out results
            self.ty.tel_blank()
            self.ty.tel_gc()
            self.ty.tel_rej()
            # self.ty.tel_nodes(self.node_list, "last")
            self.tr.cal_lat_percentile()
            self.tr.dump_meta_result(policy)
            self.tr.dump_lat_result(policy)

            # reset the internal node_list
            self.node_list = copy.deepcopy(node_list)
            self.ty.reduce_node_snap()
            print(np.percentile(node_heatings, 99))
        if len(policies) > 1:
            baseline = None
            for i, data in enumerate(quick_results["mean_startup_lat"]):
                if i == 0:
                    baseline = data
                else:
                    quick_results["speedup"].append(data / baseline)
        return quick_results


