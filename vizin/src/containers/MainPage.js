
import React, { Component } from 'react'
import InputLabel from '@material-ui/core/InputLabel'
import MenuItem from '@material-ui/core/MenuItem'
import FormControl from '@material-ui/core/FormControl'
import Select from '@material-ui/core/Select'
import Chip from '@material-ui/core/Chip';
import Input from '@material-ui/core/Input';


import { withStyles } from '@material-ui/core'
import { getTerms } from '../services/TermService'
import { getJobs } from '../services/JobService'
import moment from 'moment'
import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: theme.spacing.unit / 4,
  },
});

const LINE_COLORS=[
  '#f44336',
  "#8bc34a",
  '#e91e63',
  '#9c27b0',
  "#4caf50",

  "#795548",
  '#3f51b5',
  "#9e9e9e",
  "#2196f3",
  "#ffd600",
  "#00bcd4",
  "#009688",
  
  "#cddc39",
  "#ff9800",
  
  

]

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;

const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

class MainPage extends Component {
  constructor() {
    super()
    this.state = {
      terms: [],
      termsMultiple: [],
      term: '',
      jobs: [],
      chartData: [],
      mappedTerms: {},
      selectedTerm: null
    }
    this.getTerms = this.getTerms.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleChangeMultiple = this.handleChangeMultiple.bind(this)
    this.formatTooltip = this.formatTooltip.bind(this)
    this.updateJobList = this.updateJobList.bind(this)
  }

  async getTerms() {
    try {
      const res = await getTerms()
      let terms = []
      if (res.status == 200) {
        terms = res.data
      }
      const mappedTerms = terms.reduce((prev, curr) => {
        prev[curr.term] = curr.id
        prev[curr.id] = curr.term
        return prev
      }, {})
      this.setState({
        terms,
        mappedTerms
      })
    } catch (e) {
      console.error(e)
      throw e
    }
  }

  async getJobs(termId) {
    try {
      const res = await getJobs(termId)
      let jobs = null
      if (res.status == 200) {
        jobs = res.data
      }
      jobs = jobs.slice(-100)
      const chartData = jobs.map(job => ({
        value: job.total,
        time: moment(job.created_at).toDate().getTime()
      }))
      return chartData
    } catch (e) {
      console.error(e)
      throw e
    }
  }

  formatTooltip(value, name) {
    switch (name) {
      case 'Time':
        value = moment.utc(value).format('MMMM Do YYYY, h:mm:ss a')
        break
      case 'Value':
        name = 'Opened Jobs'
        break
    }
    return [value, name]
  }

  handleChange(event) {
    console.log(event.target)
    this.setState({ [event.target.name]: event.target.value });
    this.getJobs(event.target.value)
  }
  handleChangeMultiple({ target: { value } }) {
    this.updateJobList(value)
    this.setState({ termsMultiple: value });
  }
  async updateJobList(terms) {
    const { jobs, mappedTerms } = this.state
    const selectedTerms = terms.reduce((prev, curr) => {
      prev[curr] = true
      return prev
    }, {})
    const savedjobs = jobs.filter(job => selectedTerms[job.term])
    const added = terms.filter(term => jobs.filter(job => job.term === term).length <= 0)
    for (var term in added) {
      const newData = await this.getJobs(mappedTerms[added[term]])
      savedjobs.push({
        term: added[term],
        jobs: newData
      });
    }
    this.setState({
      jobs: savedjobs
    })
    console.log('savedJobs', savedjobs)
  }
  componentDidMount() {
    this.getTerms()
  }
  render() {
    const {
      classes
    } = this.props

    const {
      terms,
      termsMultiple,
      jobs
    } = this.state
    return (
      <div>

        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="select-multiple-chip">Term</InputLabel>
          <Select
            multiple
            value={termsMultiple}
            onChange={this.handleChangeMultiple}
            input={<Input id="select-multiple-chip" />}
            renderValue={selected => (
              <div className={classes.chips}>
                {selected.map(value => (
                  <Chip key={value} label={value} className={classes.chip} />
                ))}
              </div>
            )}
            MenuProps={MenuProps}
          >
            {terms.map(term => (
              <MenuItem key={term.term} value={term.term}>
                {term.term}
              </MenuItem>
            ))}
          </Select>
        </FormControl>



        <ResponsiveContainer width='95%' height={500} >
          <ScatterChart>
            <XAxis
              dataKey='time'
              domain={['auto', 'auto']}
              name='Time'
              tickFormatter={(tick) => moment(tick).format()}
              type='number'
            />
            <YAxis dataKey='value' name='Value' />
            <Legend />
            {
              jobs.map((term, i) => (
                <Scatter
                  data={term.jobs}
                  line={{ stroke: '#eee' }}
                  fill={LINE_COLORS[i]}
                  lineJointType='monotoneX'
                  lineType='joint'
                  name={term.term}
                />
              ))
            }

            <Tooltip cursor={{ strokeDasharray: '3 3' }} formatter={this.formatTooltip} />

          </ScatterChart>
        </ResponsiveContainer>
      </div>

    )

  }
}

export default withStyles(styles)(MainPage)