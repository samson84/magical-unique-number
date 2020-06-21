const UniqueNumber = (function () {
    async function request(url, method = 'GET', payload = null) {
        let options = {
            method: method,
            headers: {
                'content-type': 'application/json'
            }
        }

        if (payload) {
            options.body = JSON.stringify(payload)
        }
        const response = await fetch(url, options);
        try {
            const data = await response.json();
            if (data.error) {
                throw Error(`${data.error.message} (${data.error.code})`);
            }
            return data.payload;
        } catch (e) {
            console.log(e)
            throw Error(`${e}`);
        }
    }

    function updateById(list, element) {
        return list.map((current) => {
            return current.id === element.id
                ? element
                : current
        })
    }

    function getById(list, id) {
        const found = list.filter(current => current.id === id)
        return found.length > 0
            ? found[0]
            : null
    }

    function unzip(list) {
        const result = list.reduce((unzipped, current, i) => {
            unzipped[0][i] = current[0];
            unzipped[1][i] = current[1];
            return unzipped
        }, [[], []])
        return result
    }

    api = {
        async getAllRounds() { return await request('/rounds') },
        async getRound(id) { return await request(`/rounds/${id}`) },
        async startRound() { return await request('/rounds', 'POST', {}) },
        async finishRound(id) { return await request(`/rounds/${id}/finish`, 'POST', {}) },
        async vote(id, username, vote) {
            return await request(
                `/rounds/${id}/vote`,
                'POST',
                { username, vote }
            )
        },
        async getStat(id) { return await request(`/rounds/${id}/stat`) }
    }

    components = {
        Rounds() {
            return {
                isLoading: false,
                error: null,
                rounds: [],
                vote_input: '',
                username_input: '',
                vote_round_id: '',
                getAll() {
                    this.error = null;
                    this.isLoading = true;
                    api.getAllRounds()
                        .then((rounds) => this.rounds = [...rounds])
                        .catch((error) => this.error = error.message)
                        .then(() => this.isLoading = false)
                },
                getDetails(id) {
                    this.error = null;
                    this.isLoading = true;
                    api.getRound(id)
                        .then((round) => {
                            this.rounds = updateById(this.rounds, round);
                        })
                        .catch((error) => this.error = error.message)
                        .then(() => this.isLoading = false);
                },
                getStat(id) {
                    const round = getById(this.rounds, id)
                    if (round && round.stats) {
                        return;
                    }
                    this.error = null;
                    this.isLoading = true;
                    api.getStat(id)
                        .then((stats) => {
                            if (!stats.votes.length) { return; }
                            this.rounds = this.rounds.map((current) => {
                                if (current.id === id) {
                                    const [votes, occurences] = unzip(stats.votes)
                                    const updated = {
                                        ...current,
                                        stats: { votes, occurences }
                                    }
                                    return updated;
                                }
                                return current;
                            })
                            return stats;
                        })
                        .then((stats) => {
                            if (!stats.votes.length) { return; }
                            this.$nextTick(() => this.showChart(id))
                        })
                        .catch((error) => {
                            this.error = error.message;
                            console.error(error);
                        })
                        .then(() => this.isLoading = false);
                },
                showChart(id) {
                    const element = document.getElementById(`chart-${id}`);
                    const round = getById(this.rounds, id);
                    if (!round || !round.stats) { return; }
                    const votes = [...round.stats.votes]
                    const occurences = [...round.stats.occurences]
                    const chart = new Chart(element.getContext('2d'), {
                        type: 'horizontalBar',
                        data: {
                            labels: votes,
                            datasets: [{
                                label: "Occurence",
                                backgroundColor: "#3e95cd",
                                data: occurences
                            }]
                        },
                        options: {
                            scales: {
                                xAxes: [{
                                    ticks: {
                                        beginAtZero: true
                                    }
                                }]
                            }
                        }
                    });
                },
                start() {
                    this.error = null;
                    this.isLoading = true;
                    api.startRound()
                        .then((round) => {
                            this.rounds = [round, ...this.rounds]
                        })
                        .catch((error) => this.error = error.message)
                        .then(() => this.isLoading = false)
                },
                finish(id) {
                    this.error = null;
                    this.isLoading = true;
                    api.finishRound(id)
                        .then((round) => {
                            this.rounds = updateById(this.rounds, round)
                        })
                        .catch((error) => this.error = error.message)
                        .then(() => this.isLoading = false)
                },
                vote(id) {
                    this.error = null;
                    this.isLoading = true;
                    api.vote(id, this.username_input, Number(this.vote_input))
                        .then(() => {
                            this.isLoading = false
                            this.username_input = ''
                            this.vote_input = ''
                        })
                        .then(() => this.getAll())
                        .catch((error) => this.error = error.message)
                        .then(() => {
                            this.isLoading = false
                            this.username_input = ''
                            this.vote_input = ''
                        })
                },
                onUsernameChange(e) {
                    this.username_input = e.target.value
                },
                onVoteChange(e) {
                    this.vote_input = e.target.value
                }
            }
        }
    }
    return { api, components }
})()

async function main() {
    const result = await fetch('/rounds')
    const data = await result.json()
    console.log(data)
}

